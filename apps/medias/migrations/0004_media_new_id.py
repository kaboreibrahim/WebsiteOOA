from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medias', '0003_alter_media_categorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='new_id',
            field=models.UUIDField(editable=False, null=True),
        ),
    ]
