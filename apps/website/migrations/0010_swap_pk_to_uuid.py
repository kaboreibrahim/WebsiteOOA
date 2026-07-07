import uuid

from django.db import migrations, models

from core.utils.migration_helpers import swap_int_pk_to_uuid


def _state_ops(model_name):
    return [
        migrations.RemoveField(model_name=model_name, name='id'),
        migrations.RenameField(model_name=model_name, old_name='new_id', new_name='id'),
        migrations.AlterField(
            model_name=model_name,
            name='id',
            field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
        ),
    ]


class Migration(migrations.Migration):

    # Les ALTER TABLE bruts executes dans swap_int_pk_to_uuid() ne peuvent pas
    # tourner dans une transaction sur MySQL (DDL non transactionnel).
    atomic = False

    dependencies = [
        ('website', '0009_populate_new_id_uuid'),
    ]

    operations = [
        migrations.RunPython(swap_int_pk_to_uuid('website_hero'), migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(state_operations=_state_ops('hero')),

        migrations.RunPython(swap_int_pk_to_uuid('website_produit'), migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(state_operations=_state_ops('produit')),

        migrations.RunPython(swap_int_pk_to_uuid('website_contact'), migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(state_operations=_state_ops('contact')),

        migrations.RunPython(swap_int_pk_to_uuid('website_personne'), migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(state_operations=_state_ops('personne')),

        migrations.RunPython(swap_int_pk_to_uuid('website_partenaire'), migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(state_operations=_state_ops('partenaire')),
    ]
