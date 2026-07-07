from django.db import migrations, models


def _remap_forwards(apps, schema_editor):
    Article = apps.get_model('blog', 'Article')
    Categorie = apps.get_model('blog', 'Categorie')
    for article in Article.objects.all().only('pk', 'categorie_id'):
        if article.categorie_id is None:
            continue
        try:
            categorie = Categorie.objects.get(pk=article.categorie_id)
        except Categorie.DoesNotExist:
            continue
        article.new_categorie = categorie.new_id
        article.save(update_fields=['new_categorie'])


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_populate_new_id_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='new_categorie',
            field=models.UUIDField(null=True, blank=True, editable=False),
        ),
        migrations.RunPython(_remap_forwards, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='article',
            name='categorie',
        ),
    ]
