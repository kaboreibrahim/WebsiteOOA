from django.db import models


class Media(models.Model):
    TYPE_PHOTO = 'photo'
    TYPE_VIDEO = 'video'
    TYPE_CHOICES = [
        (TYPE_PHOTO, 'Photo'),
        (TYPE_VIDEO, 'Vidéo'),
    ]

    CAT_OPERATIONS  = 'operations'
    CAT_PRODUITS    = 'produits'
    CAT_SOURCING    = 'sourcing'
    CAT_LOGISTIQUE  = 'logistique'
    CAT_CHOICES = [
        (CAT_OPERATIONS, 'Opérations'),
        (CAT_PRODUITS,   'Produits'),
        (CAT_SOURCING,   'Sourcing'),
        (CAT_LOGISTIQUE, 'Logistique'),
    ]

    type        = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_PHOTO, verbose_name="Type")
    categorie   = models.CharField(max_length=20, choices=CAT_CHOICES, blank=True, default='', verbose_name="Catégorie")
    titre       = models.CharField(max_length=255, verbose_name="Titre")
    description = models.CharField(max_length=300, blank=True, verbose_name="Description courte (hover)")
    image       = models.ImageField(upload_to='medias/photos/', blank=True, null=True, verbose_name="Image")
    vignette    = models.ImageField(upload_to='medias/vignettes/', blank=True, null=True, verbose_name="Vignette vidéo")
    video_url   = models.URLField(blank=True, null=True, verbose_name="URL embed YouTube / Vimeo")
    en_vedette  = models.BooleanField(default=False, verbose_name="En vedette (vidéo principale)")
    actif       = models.BooleanField(default=True, verbose_name="Actif")
    ordre       = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name        = "Média"
        verbose_name_plural = "Médias"
        ordering            = ['ordre']

    def __str__(self):
        return f"[{self.get_type_display()}] {self.titre}"

    @property
    def thumbnail(self):
        if self.type == self.TYPE_VIDEO and self.vignette:
            return self.vignette
        return self.image
