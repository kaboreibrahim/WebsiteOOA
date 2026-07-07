import uuid

from django.db import migrations, models

from core.utils.migration_helpers import swap_int_pk_to_uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_remap_article_categorie_fk'),
    ]

    operations = [
        migrations.RunPython(swap_int_pk_to_uuid('blog_categorie'), migrations.RunPython.noop),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RemoveField(model_name='categorie', name='id'),
                migrations.RenameField(model_name='categorie', old_name='new_id', new_name='id'),
                migrations.AlterField(
                    model_name='categorie',
                    name='id',
                    field=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, serialize=False),
                ),
            ],
        ),
    ]
