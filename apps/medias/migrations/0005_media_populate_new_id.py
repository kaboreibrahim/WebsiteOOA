import uuid

from django.db import migrations


def populate_new_id(apps, schema_editor):
    Media = apps.get_model('medias', 'Media')
    for obj in Media.objects.all().only('pk'):
        obj.new_id = uuid.uuid4()
        obj.save(update_fields=['new_id'])


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0004_media_new_id'),
    ]

    operations = [
        migrations.RunPython(populate_new_id, migrations.RunPython.noop),
    ]
