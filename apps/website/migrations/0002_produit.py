from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom du produit')),
                ('description', models.TextField(verbose_name='Description')),
                ('image', models.ImageField(upload_to='produits/', verbose_name='Image')),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('ordre', models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Produit',
                'verbose_name_plural': 'Produits',
                'ordering': ['ordre'],
            },
        ),
    ]
