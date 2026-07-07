import uuid

from django.db import models


class Personne(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Role(models.TextChoices):
        DIRIGEANT = 'dirigeant', 'Dirigeant principal'
        MEMBRE    = 'membre',    'Autre membre'

    class Departement(models.TextChoices):
        AUCUN          = '',               '—'
        SOURCING       = 'sourcing',       'Sourcing'
        OPERATIONNEL   = 'operationnel',   'Opérationnel'
        ADMINISTRATIF  = 'administratif',  'Administratif'

    nom          = models.CharField(max_length=150, verbose_name="Nom complet")
    profession   = models.CharField(max_length=150, verbose_name="Poste / Profession")
    mail         = models.EmailField(verbose_name="Adresse e-mail")
    photo        = models.ImageField(upload_to='personnel/', blank=True, null=True, verbose_name="Photo")
    role         = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBRE, verbose_name="Rôle")
    departement  = models.CharField(max_length=20, choices=Departement.choices, blank=True, default='', verbose_name="Département")
    icone        = models.CharField(max_length=60, blank=True, default='person', verbose_name="Icône Material (membres)")
    ordre        = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    actif        = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        verbose_name        = "Personne"
        verbose_name_plural = "Personnel"
        ordering            = ['ordre']

    def __str__(self):
        return f"{self.nom} – {self.profession}"
