from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'apps.website'

    def ready(self):
        # Branche l'optimisation automatique des images (WebP, compression,
        # redimensionnement) sur tous les modeles du projet possedant un
        # ImageField. Fait ici car cette app est toujours chargee au demarrage.
        from core.utils.image_signals import connect_image_optimization_signals
        connect_image_optimization_signals()
