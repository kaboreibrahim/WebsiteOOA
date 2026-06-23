from django.db import models


class Hero(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre (H1)")
    description = models.TextField(verbose_name="Description (paragraphe)")
    image = models.ImageField(upload_to='hero/', verbose_name="Image de fond")
    actif = models.BooleanField(default=True, verbose_name="Actif")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name = "Hero"
        verbose_name_plural = "Heroes"
        ordering = ['ordre']

    def __str__(self):
        return self.titre
