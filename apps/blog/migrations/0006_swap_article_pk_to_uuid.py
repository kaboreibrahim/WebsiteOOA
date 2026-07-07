import uuid

from django.db import migrations, models

from core.utils.migration_helpers import swap_int_pk_to_uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_swap_categorie_pk_to_uuid'),
    ]

    operations = [
        migrations.RunPython(swap_int_pk_to_uuid('blog_article'), migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(model_name='article', name='id'),
                migrations.RenameField(model_name='article', old_name='new_id', new_name='id'),
                migrations.AlterField(
                    model_name='article',
                    name='id',
                    field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
                ),
            ],
        ),
    ]
