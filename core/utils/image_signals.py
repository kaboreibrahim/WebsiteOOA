"""
Branchement automatique de l'optimisation d'image sur tous les modeles du
projet possedant un ``ImageField``, sans avoir a modifier chaque modele.

``connect_image_optimization_signals`` est appelee une seule fois depuis
``AppConfig.ready()`` (voir ``apps/website/apps.py``). Elle inspecte tous les
modeles installes et connecte un receveur ``pre_save`` uniquement sur ceux qui
possedent au moins un ``ImageField``.

Le receveur n'agit que lorsqu'un fichier vient d'etre affecte au champ et n'est
pas encore ecrit sur le stockage (``FieldFile._committed is False``) : un
``save()`` qui ne touche pas a l'image n'est donc jamais retraite.
"""
import logging

from django.apps import apps
from django.db.models import ImageField
from django.db.models.signals import pre_save

from core.utils.image_optimizer import ImageOptimizationError, optimize_uploaded_file

logger = logging.getLogger(__name__)

_connected = False


def _image_fields(model):
    return [f for f in model._meta.get_fields() if isinstance(f, ImageField)]


def _optimize_pending_image_fields(sender, instance, **kwargs):
    for field in _image_fields(sender):
        field_file = getattr(instance, field.name)

        # Pas de fichier, ou fichier deja present sur le stockage (aucun
        # nouvel upload sur ce save) : rien a faire.
        if not field_file or getattr(field_file, "_committed", True):
            continue

        try:
            optimized_content, new_name = optimize_uploaded_file(field_file.file)
        except ImageOptimizationError:
            logger.exception(
                "Optimisation impossible pour %s.%s (pk=%s) - fichier original conserve.",
                sender.__name__, field.name, instance.pk,
            )
            continue

        if optimized_content is None:
            # Extension non prise en charge (ex: .gif animes) -> on laisse
            # Django enregistrer le fichier original sans le transformer.
            continue

        field_file.save(new_name, optimized_content, save=False)


def connect_image_optimization_signals():
    """A appeler une seule fois au demarrage de l'application (idempotent)."""
    global _connected
    if _connected:
        return

    for model in apps.get_models():
        if _image_fields(model):
            pre_save.connect(_optimize_pending_image_fields, sender=model, weak=False)

    _connected = True
