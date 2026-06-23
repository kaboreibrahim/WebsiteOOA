from django.db import models


class Contact(models.Model):
    SUJET_CHOICES = [
        ('devis', 'Demande de devis'),
        ('logistique', 'Logistique / Flexitanks'),
        ('sourcing', 'Sourcing / Partenariat'),
        ('autre', 'Autre'),
    ]

    nom = models.CharField(max_length=255, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    sujet = models.CharField(max_length=50, choices=SUJET_CHOICES, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    date_envoi = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    lu = models.BooleanField(default=False, verbose_name="Lu")

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_envoi']

    def __str__(self):
        return f"{self.nom} — {self.get_sujet_display()} ({self.date_envoi:%d/%m/%Y})"
