from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_produit_categorie_produit_conditionnement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='hero',
            name='new_id',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='produit',
            name='new_id',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='contact',
            name='new_id',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='personne',
            name='new_id',
            field=models.UUIDField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='partenaire',
            name='new_id',
            field=models.UUIDField(editable=False, null=True),
        ),
    ]
