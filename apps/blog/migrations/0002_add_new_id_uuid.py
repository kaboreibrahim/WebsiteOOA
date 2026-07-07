from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_categorie_article'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='new_id',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='new_id',
            field=models.UUIDField(editable=False, null=True),
        ),
    ]
