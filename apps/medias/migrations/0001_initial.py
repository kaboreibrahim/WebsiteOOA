from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('photo', 'Photo'), ('video', 'Vidéo')], default='photo', max_length=10, verbose_name='Type')),
                ('titre', models.CharField(max_length=255, verbose_name='Titre / description alt')),
                ('image', models.ImageField(blank=True, null=True, upload_to='medias/photos/', verbose_name='Image (pour les photos)')),
                ('video_url', models.URLField(blank=True, null=True, verbose_name='URL de la vidéo (YouTube / Vimeo embed)')),
                ('actif', models.BooleanField(default=True, verbose_name='Actif')),
                ('ordre', models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")),
            ],
            options={
                'verbose_name': 'Média',
                'verbose_name_plural': 'Médias',
                'ordering': ['ordre'],
            },
        ),
    ]
