import uuid

from django.db import migrations


def _populate(model_name):
    def _forwards(apps, schema_editor):
        Model = apps.get_model('blog', model_name)
        for obj in Model.objects.all().only('pk'):
            obj.new_id = uuid.uuid4()
            obj.save(update_fields=['new_id'])
    return _forwards


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_add_new_id_uuid'),
    ]

    operations = [
        migrations.RunPython(_populate('Categorie'), migrations.RunPython.noop),
        migrations.RunPython(_populate('Article'), migrations.RunPython.noop),
    ]
