import uuid

from django.db import migrations, models

from core.utils.migration_helpers import swap_int_pk_to_uuid


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0005_media_populate_new_id'),
    ]

    operations = [
        migrations.RunPython(
            swap_int_pk_to_uuid('medias_media'),
            migrations.RunPython.noop,
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(
                    model_name='media',
                    name='id',
                ),
                migrations.RenameField(
                    model_name='media',
                    old_name='new_id',
                    new_name='id',
                ),
                migrations.AlterField(
                    model_name='media',
                    name='id',
                    field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
                ),
            ],
        ),
    ]
