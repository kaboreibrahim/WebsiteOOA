import uuid

from django.db import migrations


def _populate(model_name):
    def _forwards(apps, schema_editor):
        Model = apps.get_model('website', model_name)
        for obj in Model.objects.all().only('pk'):
            obj.new_id = uuid.uuid4()
            obj.save(update_fields=['new_id'])
    return _forwards


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_add_new_id_uuid'),
    ]

    operations = [
        migrations.RunPython(_populate('Hero'), migrations.RunPython.noop),
        migrations.RunPython(_populate('Produit'), migrations.RunPython.noop),
        migrations.RunPython(_populate('Contact'), migrations.RunPython.noop),
        migrations.RunPython(_populate('Personne'), migrations.RunPython.noop),
        migrations.RunPython(_populate('Partenaire'), migrations.RunPython.noop),
    ]
