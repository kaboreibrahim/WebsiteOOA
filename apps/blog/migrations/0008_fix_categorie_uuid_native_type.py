import uuid as uuid_lib

from django.db import migrations


def _fix_categorie_id_type(apps, schema_editor):
    """
    Une premiere tentative de migration (avant correction du helper) a
    converti blog_categorie.id en char(32) hexadecimal (sans tirets) au lieu
    du type natif `uuid` que MariaDB >= 10.7 propose et que Django utilise
    pour UUIDField sur ce serveur. On reconvertit chaque valeur au format
    UUID canonique puis on retablit le type de colonne natif.

    Ne fait rien si la colonne est deja au bon type (MySQL sans support UUID
    natif, ou execution repetee/ide potente).
    """
    if schema_editor.connection.vendor != 'mysql':
        return
    if not schema_editor.connection.features.has_native_uuid_field:
        return

    cursor = schema_editor.connection.cursor()
    cursor.execute(
        "SELECT DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS "
        "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME='blog_categorie' AND COLUMN_NAME='id'"
    )
    row = cursor.fetchone()
    if row is None or row[0] == 'uuid':
        return  # deja au bon format, rien a faire

    cursor.execute("SELECT id FROM blog_categorie")
    rows = cursor.fetchall()

    schema_editor.execute("ALTER TABLE `blog_categorie` ADD COLUMN `id_fixed` uuid NULL")
    for (raw_id,) in rows:
        canonical = str(uuid_lib.UUID(hex=raw_id))
        cursor.execute(
            "UPDATE `blog_categorie` SET `id_fixed` = %s WHERE `id` = %s",
            [canonical, raw_id],
        )
    schema_editor.execute("ALTER TABLE `blog_categorie` DROP PRIMARY KEY")
    schema_editor.execute("ALTER TABLE `blog_categorie` DROP COLUMN `id`")
    schema_editor.execute("ALTER TABLE `blog_categorie` CHANGE `id_fixed` `id` uuid NOT NULL")
    schema_editor.execute("ALTER TABLE `blog_categorie` ADD PRIMARY KEY (`id`)")


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('blog', '0007_finalize_article_categorie_fk'),
    ]

    operations = [
        migrations.RunPython(_fix_categorie_id_type, migrations.RunPython.noop),
    ]
