import uuid

from django.db import models
from django.utils.text import slugify


class Categorie(models.Model):
    id   = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom  = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name        = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering            = ['nom']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom


class Article(models.Model):
    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    titre            = models.CharField(max_length=255, verbose_name="Titre")
    slug             = models.SlugField(max_length=255, unique=True, blank=True)
    image_hero       = models.ImageField(upload_to='blog/', verbose_name="Image principale")
    extrait          = models.TextField(max_length=300, verbose_name="Extrait / Résumé")
    contenu          = models.TextField(verbose_name="Contenu (HTML ou texte)")
    categorie        = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='articles', verbose_name="Catégorie")
    auteur           = models.CharField(max_length=150, default='Oils of Africa', verbose_name="Auteur")
    date_publication = models.DateField(verbose_name="Date de publication")
    temps_lecture    = models.PositiveIntegerField(default=5, verbose_name="Temps de lecture (min)")
    en_une           = models.BooleanField(default=False, verbose_name="Article à la une")
    actif            = models.BooleanField(default=True, verbose_name="Publié")

    class Meta:
        verbose_name        = "Article"
        verbose_name_plural = "Articles"
        ordering            = ['-date_publication']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titre
