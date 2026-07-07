"""
Optimisation centralisee des images du projet (Pillow).

Ce module contient toute la logique de traitement d'image : conversion WebP,
compression, redimensionnement, suppression des metadonnees EXIF et gestion
de la transparence. Il est utilise a la fois par :

- les signaux Django (voir ``core.utils.image_signals``) qui optimisent
  automatiquement toute nouvelle image envoyee via l'admin, un formulaire
  ou un upload utilisateur ;
- la commande de management ``optimize_images`` qui convertit le parc
  d'images deja present en base/media.

Rien ici ne depend de l'ORM Django : ces fonctions manipulent uniquement des
octets/fichiers et peuvent donc etre testees et reutilisees independamment.
"""
from __future__ import annotations

import os
from io import BytesIO

from django.conf import settings
from django.core.files.base import ContentFile
from PIL import Image, ImageOps

# Extensions sources que l'on accepte d'optimiser. Les GIF (animations) et les
# SVG (vectoriel) sont volontairement exclus pour ne pas casser leur usage.
SUPPORTED_INPUT_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"}

DEFAULT_MAX_DIMENSION = 1920
DEFAULT_QUALITY = 85
DEFAULT_METHOD = 6  # methode de compression WebP : 0 (rapide) a 6 (optimale)

OUTPUT_FORMAT = "WEBP"
OUTPUT_EXTENSION = ".webp"


class ImageOptimizationError(Exception):
    """Levee lorsqu'une image ne peut pas etre ouverte ou convertie."""


def _setting(name: str, default):
    return getattr(settings, name, default)


def is_already_webp(filename: str) -> bool:
    """True si le fichier est deja au format WebP."""
    return filename.lower().endswith(OUTPUT_EXTENSION)


def is_optimizable(filename: str) -> bool:
    """True si l'extension du fichier fait partie des formats pris en charge."""
    ext = os.path.splitext(filename)[1].lower()
    return ext in SUPPORTED_INPUT_EXTENSIONS


def build_webp_filename(original_filename: str) -> str:
    """Remplace l'extension du fichier par ``.webp`` en conservant le nom de base."""
    base, _ext = os.path.splitext(original_filename)
    return f"{base}{OUTPUT_EXTENSION}"


def _resize_if_needed(image: Image.Image, max_dimension: int) -> Image.Image:
    """Redimensionne l'image si besoin, en conservant les proportions."""
    if max(image.size) <= max_dimension:
        return image
    resized = image.copy()
    resized.thumbnail((max_dimension, max_dimension), Image.LANCZOS)
    return resized


def _prepare_color_mode(image: Image.Image) -> Image.Image:
    """
    Normalise le mode couleur pour l'export WebP en preservant la transparence
    (RGBA) des PNG/GIF/WebP qui en possedent, et en convertissant le reste en RGB.
    """
    has_transparency = image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    )
    if has_transparency:
        return image.convert("RGBA")
    if image.mode != "RGB":
        return image.convert("RGB")
    return image


def optimize_image_bytes(
    source,
    *,
    max_dimension: int | None = None,
    quality: int | None = None,
    method: int | None = None,
) -> tuple[bytes, int, int]:
    """
    Optimise une image et retourne ``(contenu_webp, largeur, hauteur)``.

    ``source`` peut etre un chemin, un objet fichier ouvert en binaire, ou tout
    objet accepte par ``PIL.Image.open``. Les metadonnees EXIF ne sont pas
    recopiees dans le fichier de sortie (WebP ne conserve que ce qu'on y ecrit
    explicitement), ce qui les supprime de fait tout en respectant l'orientation
    d'origine de la photo.

    Leve ``ImageOptimizationError`` si le fichier n'est pas une image valide.
    """
    max_dimension = max_dimension or _setting("IMAGE_OPTIMIZER_MAX_DIMENSION", DEFAULT_MAX_DIMENSION)
    quality = quality or _setting("IMAGE_OPTIMIZER_QUALITY", DEFAULT_QUALITY)
    method = _setting("IMAGE_OPTIMIZER_METHOD", DEFAULT_METHOD) if method is None else method

    try:
        with Image.open(source) as original:
            # Applique la rotation EXIF avant de la jeter, sinon les photos
            # prises verticalement se retrouveraient couchees.
            image = ImageOps.exif_transpose(original)
            if image is None:
                image = original
            image = _prepare_color_mode(image)
            image = _resize_if_needed(image, max_dimension)

            buffer = BytesIO()
            image.save(
                buffer,
                format=OUTPUT_FORMAT,
                quality=quality,
                method=method,
                optimize=True,
                lossless=False,
            )
            return buffer.getvalue(), image.width, image.height
    except ImageOptimizationError:
        raise
    except Exception as exc:
        # PIL leve des exceptions variees selon le probleme (fichier corrompu,
        # format non reconnu, IO...) ; on les uniformise pour les appelants.
        raise ImageOptimizationError(f"Impossible d'optimiser l'image : {exc}") from exc


def optimize_uploaded_file(
    django_file,
    *,
    max_dimension: int | None = None,
    quality: int | None = None,
    method: int | None = None,
) -> tuple[ContentFile | None, str | None]:
    """
    Optimise un fichier Django (``UploadedFile``/``File``) et retourne un
    ``ContentFile`` WebP pret a etre affecte a un ``ImageField``, ainsi que
    son nouveau nom de fichier.

    Retourne ``(None, None)`` si le fichier n'a pas une extension prise en
    charge (le fichier original est alors conserve tel quel par l'appelant).
    """
    name = getattr(django_file, "name", "") or ""
    if not is_optimizable(name):
        return None, None

    if hasattr(django_file, "seek"):
        django_file.seek(0)

    content_bytes, _width, _height = optimize_image_bytes(
        django_file, max_dimension=max_dimension, quality=quality, method=method,
    )
    new_name = build_webp_filename(os.path.basename(name))
    return ContentFile(content_bytes, name=new_name), new_name
