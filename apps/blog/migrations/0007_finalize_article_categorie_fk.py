import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_swap_article_pk_to_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='new_categorie',
            new_name='categorie',
        ),
        migrations.AlterField(
            model_name='article',
            name='categorie',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='articles',
                to='blog.categorie',
                verbose_name='Catégorie',
            ),
        ),
    ]
