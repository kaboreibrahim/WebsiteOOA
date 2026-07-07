"""
Aide reutilisable pour remplacer une PK entiere auto-incrementee par un UUID
sur une table Django deja peuplee (SQLite et MySQL).

Le schema-editor de Django presente une limitation connue sur SQLite : toute
tentative d'AlterField/RenameField sur le champ historique marque comme PK
auto-creee (`auto_created=True`) declenche une reconstruction de table
buguee qui duplique la colonne "id" dans le CREATE TABLE genere. On
contourne donc ce probleme en executant du SQL brut propre a chaque moteur,
puis en synchronisant l'etat de migration Django via
`SeparateDatabaseAndState` (voir les migrations `..._swap_pk_to_uuid.py`).
"""


def swap_int_pk_to_uuid(table_name, uuid_column="new_id", id_column="id"):
    """
    Retourne une fonction utilisable dans un ``migrations.RunPython`` qui :
    - supprime `id_column` (l'ancien entier auto-incremente, encore PK) ;
    - promeut `uuid_column` (deja rempli et rendu unique par une migration
      precedente) au rang de nouvelle PK, renommee `id_column`.
    """

    def _forwards(apps, schema_editor):
        vendor = schema_editor.connection.vendor
        if vendor == "sqlite":
            _swap_sqlite(schema_editor, table_name, uuid_column, id_column)
        elif vendor == "mysql":
            _swap_mysql(schema_editor, table_name, uuid_column, id_column)
        else:
            raise NotImplementedError(
                f"Swap de PK UUID non pris en charge pour le moteur '{vendor}'."
            )

    return _forwards


def _swap_mysql(schema_editor, table, uuid_column, id_column):
    execute = schema_editor.execute
    cursor = schema_editor.connection.cursor()

    # MariaDB >= 10.7 a un type colonne "uuid" natif que Django utilise pour
    # UUIDField ; sur les autres moteurs (MySQL, ou MariaDB plus ancien) le
    # type reste char(32). Ne JAMAIS forcer char(32) en dur : ca desynchronise
    # le type reel de la colonne de ce que Django ecrit/lit ensuite.
    uuid_type = "uuid" if schema_editor.connection.features.has_native_uuid_field else "char(32)"

    # Idempotent : si une tentative precedente a deja supprime l'ancienne
    # colonne entiere avant d'echouer plus loin, on ne rejoue pas cette partie.
    cursor.execute(
        "SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME=%s AND COLUMN_NAME=%s",
        [table, id_column],
    )
    old_id_still_present = cursor.fetchone()[0] > 0

    if old_id_still_present:
        execute(f"ALTER TABLE `{table}` MODIFY `{id_column}` BIGINT NOT NULL")
        execute(f"ALTER TABLE `{table}` DROP PRIMARY KEY")
        execute(f"ALTER TABLE `{table}` DROP COLUMN `{id_column}`")

    execute(f"ALTER TABLE `{table}` CHANGE `{uuid_column}` `{id_column}` {uuid_type} NOT NULL")
    execute(f"ALTER TABLE `{table}` ADD PRIMARY KEY (`{id_column}`)")


def _swap_sqlite(schema_editor, table, uuid_column, id_column):
    cursor = schema_editor.connection.cursor()
    cursor.execute(f"PRAGMA table_info('{table}')")
    columns = cursor.fetchall()  # (cid, name, type, notnull, dflt_value, pk)

    col_defs = []
    target_names = []  # noms des colonnes dans la nouvelle table
    source_names = []  # noms correspondants a lire dans l'ancienne table
    for _cid, name, ctype, notnull, dflt, _pk in columns:
        if name == id_column:
            continue  # ancienne colonne entiere : supprimee
        source_names.append(name)
        if name == uuid_column:
            # la colonne uuid devient la PK, renommee id_column au passage
            target_names.append(id_column)
            col_defs.append(f'"{id_column}" char(32) NOT NULL PRIMARY KEY')
        else:
            target_names.append(name)
            parts = [f'"{name}"', ctype or "text"]
            if notnull:
                parts.append("NOT NULL")
            if dflt is not None:
                parts.append(f"DEFAULT {dflt}")
            col_defs.append(" ".join(parts))

    tmp_table = f"new__{table}"
    schema_editor.execute(f'CREATE TABLE "{tmp_table}" ({", ".join(col_defs)})')
    target_csv = ", ".join(f'"{c}"' for c in target_names)
    source_csv = ", ".join(f'"{c}"' for c in source_names)
    schema_editor.execute(
        f'INSERT INTO "{tmp_table}" ({target_csv}) SELECT {source_csv} FROM "{table}"'
    )
    schema_editor.execute(f'DROP TABLE "{table}"')
    schema_editor.execute(f'ALTER TABLE "{tmp_table}" RENAME TO "{table}"')
