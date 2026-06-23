from django.db import models


class Produit(models.Model):

    CAT_PALME       = 'palme'
    CAT_TROPICAL    = 'tropical'
    CAT_INDUSTRIEL  = 'industriel'
    CAT_CHOICES = [
        (CAT_PALME,      'Palme & dérivés'),
        (CAT_TROPICAL,   'Huiles tropicales'),
        (CAT_INDUSTRIEL, 'Industriels'),
    ]

    nom              = models.CharField(max_length=255, verbose_name="Nom du produit")
    categorie        = models.CharField(max_length=20, choices=CAT_CHOICES, default=CAT_PALME, verbose_name="Catégorie")
    description      = models.TextField(verbose_name="Description")
    image            = models.ImageField(upload_to='produits/', blank=True, null=True, verbose_name="Image")

    # Spécifications techniques
    ffa              = models.CharField(max_length=50,  blank=True, verbose_name="FFA")
    iv               = models.CharField(max_length=50,  blank=True, verbose_name="Indice d'iode (IV)")
    point_fusion     = models.CharField(max_length=50,  blank=True, verbose_name="Point de fusion")
    conditionnement  = models.CharField(max_length=100, blank=True, verbose_name="Conditionnement")
    origine          = models.CharField(max_length=100, blank=True, verbose_name="Origine(s)")
    lead_time        = models.CharField(max_length=50,  blank=True, verbose_name="Lead time")
    usage            = models.CharField(max_length=100, blank=True, verbose_name="Usage")

    actif            = models.BooleanField(default=True, verbose_name="Actif")
    ordre            = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    class Meta:
        verbose_name        = "Produit"
        verbose_name_plural = "Produits"
        ordering            = ['ordre']

    def __str__(self):
        return self.nom

    @property
    def specs(self):
        """Retourne la liste des spécifications non vides."""
        fields = [
            ('FFA',           self.ffa),
            ('IV',            self.iv),
            ('Point de fusion', self.point_fusion),
            ('Conditionnement', self.conditionnement),
            ('Origine',       self.origine),
            ('Usage',         self.usage),
        ]
        return [(k, v) for k, v in fields if v]
