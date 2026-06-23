from django.db import models


class Partenaire(models.Model):
    nom    = models.CharField(max_length=200, verbose_name="Nom du partenaire")
    logo   = models.ImageField(upload_to='partenaires/', verbose_name="Logo")
    lien   = models.URLField(blank=True, verbose_name="Site web")
    ordre  = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    actif  = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name        = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering            = ['ordre']

    def __str__(self):
        return self.nom
