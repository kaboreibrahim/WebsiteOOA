from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_produit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255, verbose_name='Nom complet')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('sujet', models.CharField(
                    choices=[
                        ('devis', 'Demande de devis'),
                        ('logistique', 'Logistique / Flexitanks'),
                        ('sourcing', 'Sourcing / Partenariat'),
                        ('autre', 'Autre'),
                    ],
                    max_length=50,
                    verbose_name='Sujet',
                )),
                ('message', models.TextField(verbose_name='Message')),
                ('date_envoi', models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")),
                ('lu', models.BooleanField(default=False, verbose_name='Lu')),
            ],
            options={
                'verbose_name': 'Message de contact',
                'verbose_name_plural': 'Messages de contact',
                'ordering': ['-date_envoi'],
            },
        ),
    ]
