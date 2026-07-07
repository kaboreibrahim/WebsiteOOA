"""
Commande de management : convertit en WebP toutes les images deja stockees
en base/media, pour tous les modeles du projet possedant un ImageField.

Usage :
    python manage.py optimize_images
    python manage.py optimize_images --dry-run
    python manage.py optimize_images --quality 80 --max-dimension 1600
"""
import os

from django.apps import apps
from django.core.management.base import BaseCommand
from django.db.models import ImageField

from core.utils.image_optimizer import (
    ImageOptimizationError,
    build_webp_filename,
    is_already_webp,
    is_optimizable,
    optimize_image_bytes,
)


class Command(BaseCommand):
    help = (
        "Convertit en WebP toutes les images existantes (tous modeles avec "
        "ImageField), compresse/redimensionne, met a jour la base et supprime "
        "l'ancien fichier une fois la conversion validee."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true",
            help="N'ecrit et ne supprime rien, affiche seulement ce qui serait fait.",
        )
        parser.add_argument("--quality", type=int, default=None, help="Qualite WebP (0-100).")
        parser.add_argument(
            "--max-dimension", type=int, default=None,
            help="Plus grand cote autorise, en pixels.",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        quality = options["quality"]
        max_dimension = options["max_dimension"]

        targets = self._collect_targets()
        total = len(targets)

        if total == 0:
            self.stdout.write(self.style.WARNING("Aucune image trouvee a traiter."))
            return

        self.stdout.write(f"{total} image(s) a examiner...\n")

        stats = {"converted": 0, "already_webp": 0, "missing": 0, "unsupported": 0, "errors": 0}

        for index, (instance, field) in enumerate(targets, start=1):
            self._print_progress(index, total)
            self._process_one(instance, field, dry_run, quality, max_dimension, stats)

        self.stdout.write("\n")
        self.stdout.write(self.style.SUCCESS(
            "Termine. "
            f"Convertis: {stats['converted']} | "
            f"Deja WebP: {stats['already_webp']} | "
            f"Fichiers manquants: {stats['missing']} | "
            f"Formats ignores: {stats['unsupported']} | "
            f"Erreurs: {stats['errors']}"
        ))

    def _collect_targets(self):
        """Retourne la liste des (instance, field) pour chaque ImageField renseigne."""
        targets = []
        for model in apps.get_models():
            image_fields = [f for f in model._meta.get_fields() if isinstance(f, ImageField)]
            if not image_fields:
                continue
            for field in image_fields:
                queryset = (
                    model._base_manager
                    .exclude(**{field.name: ""})
                    .exclude(**{f"{field.name}__isnull": True})
                )
                for instance in queryset.iterator():
                    targets.append((instance, field))
        return targets

    def _process_one(self, instance, field, dry_run, quality, max_dimension, stats):
        field_file = getattr(instance, field.name)
        name = field_file.name

        if not name:
            stats["missing"] += 1
            return

        if is_already_webp(name):
            stats["already_webp"] += 1
            return

        if not is_optimizable(name):
            stats["unsupported"] += 1
            return

        storage = field_file.storage
        if not storage.exists(name):
            self.stderr.write(f"\nFichier manquant, ignore : {name}")
            stats["missing"] += 1
            return

        try:
            with storage.open(name, "rb") as fh:
                content_bytes, _w, _h = optimize_image_bytes(
                    fh, max_dimension=max_dimension, quality=quality,
                )
        except ImageOptimizationError as exc:
            self.stderr.write(f"\nErreur de conversion sur {name} : {exc}")
            stats["errors"] += 1
            return

        new_name = build_webp_filename(os.path.basename(name))

        if dry_run:
            self.stdout.write(f"\n[dry-run] {name} -> {new_name}")
            stats["converted"] += 1
            return

        old_name = name
        try:
            from django.core.files.base import ContentFile
            field_file.save(new_name, ContentFile(content_bytes), save=False)
            model = type(instance)
            model._base_manager.filter(pk=instance.pk).update(**{field.name: field_file.name})
        except Exception as exc:
            self.stderr.write(f"\nErreur d'enregistrement pour {name} : {exc}")
            stats["errors"] += 1
            return

        # On ne supprime l'ancien fichier qu'une fois la conversion ET la
        # mise a jour de la base confirmees.
        try:
            if storage.exists(old_name):
                storage.delete(old_name)
        except Exception:
            self.stderr.write(f"\nConversion OK mais impossible de supprimer l'ancien fichier : {old_name}")

        stats["converted"] += 1

    def _print_progress(self, current, total):
        width = 30
        filled = int(width * current / total)
        bar = "#" * filled + "-" * (width - filled)
        self.stdout.write(f"\r[{bar}] {current}/{total}", ending="")
        self.stdout.flush()
