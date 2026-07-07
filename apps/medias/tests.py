import unittest
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image

from core.utils.image_optimizer import (
    build_webp_filename,
    is_already_webp,
    is_optimizable,
    optimize_image_bytes,
    optimize_uploaded_file,
)

from apps.medias.models import Media


def _make_image_bytes(size, mode="RGB", color=(255, 0, 0), fmt="PNG"):
    image = Image.new(mode, size, color)
    buffer = BytesIO()
    image.save(buffer, format=fmt)
    buffer.seek(0)
    return buffer


class ImageOptimizerHelpersTests(unittest.TestCase):
    """Tests unitaires purs (aucun acces DB) sur les fonctions utilitaires."""

    def test_is_already_webp(self):
        self.assertTrue(is_already_webp("photo.webp"))
        self.assertTrue(is_already_webp("PHOTO.WEBP"))
        self.assertFalse(is_already_webp("photo.png"))

    def test_is_optimizable(self):
        self.assertTrue(is_optimizable("photo.jpg"))
        self.assertTrue(is_optimizable("photo.PNG"))
        self.assertFalse(is_optimizable("animation.gif"))
        self.assertFalse(is_optimizable("logo.svg"))

    def test_build_webp_filename(self):
        self.assertEqual(build_webp_filename("photo.jpg"), "photo.webp")
        self.assertEqual(build_webp_filename("dossier/photo.PNG"), "dossier/photo.webp")


class OptimizeImageBytesTests(unittest.TestCase):
    """Tests unitaires purs sur la conversion Pillow (pas de DB requise)."""

    def test_converts_to_webp(self):
        source = _make_image_bytes((100, 100), fmt="PNG")
        content, width, height = optimize_image_bytes(source)
        self.assertEqual((width, height), (100, 100))
        # Signature de fichier WebP : "RIFF....WEBP"
        self.assertEqual(content[:4], b"RIFF")
        self.assertEqual(content[8:12], b"WEBP")

    def test_resizes_while_keeping_aspect_ratio(self):
        source = _make_image_bytes((4000, 2000), fmt="JPEG")
        content, width, height = optimize_image_bytes(source, max_dimension=1920)
        self.assertEqual(width, 1920)
        self.assertEqual(height, 960)  # ratio 2:1 conserve

    def test_does_not_upscale_small_images(self):
        source = _make_image_bytes((300, 200), fmt="JPEG")
        _content, width, height = optimize_image_bytes(source, max_dimension=1920)
        self.assertEqual((width, height), (300, 200))

    def test_preserves_png_transparency(self):
        image = Image.new("RGBA", (50, 50), (10, 20, 30, 128))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        content, _width, _height = optimize_image_bytes(buffer)

        result = Image.open(BytesIO(content))
        self.assertEqual(result.mode, "RGBA")
        self.assertEqual(result.getpixel((0, 0))[3], 128)

    def test_opaque_png_is_converted_to_rgb(self):
        image = Image.new("RGBA", (20, 20), (10, 20, 30, 255))
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        content, _width, _height = optimize_image_bytes(buffer)

        result = Image.open(BytesIO(content))
        self.assertEqual(result.mode, "RGB")

    def test_invalid_image_raises_optimization_error(self):
        from core.utils.image_optimizer import ImageOptimizationError

        with self.assertRaises(ImageOptimizationError):
            optimize_image_bytes(BytesIO(b"not an image"))


class OptimizeUploadedFileTests(unittest.TestCase):
    def test_unsupported_extension_is_ignored(self):
        upload = SimpleUploadedFile("animation.gif", b"fake-gif-bytes", content_type="image/gif")
        content, new_name = optimize_uploaded_file(upload)
        self.assertIsNone(content)
        self.assertIsNone(new_name)

    def test_supported_extension_returns_webp_content_file(self):
        source = _make_image_bytes((64, 64), fmt="PNG")
        upload = SimpleUploadedFile("photo.png", source.read(), content_type="image/png")
        content, new_name = optimize_uploaded_file(upload)
        self.assertEqual(new_name, "photo.webp")
        self.assertIsNotNone(content)


class MediaModelAutoOptimizationTests(TestCase):
    """
    Verifie que le signal pre_save optimise automatiquement l'image au
    moment du save() d'un modele metier, sans code specifique au modele.
    """

    def _uploaded_png(self, name="photo.png", size=(2400, 1200)):
        buffer = _make_image_bytes(size, fmt="PNG")
        return SimpleUploadedFile(name, buffer.read(), content_type="image/png")

    def test_new_upload_is_converted_to_webp_and_resized(self):
        media = Media.objects.create(
            titre="Test",
            type=Media.TYPE_PHOTO,
            image=self._uploaded_png(),
        )
        try:
            self.assertTrue(media.image.name.endswith(".webp"))
            with media.image.open("rb") as fh:
                stored = Image.open(fh)
                stored.load()
                self.assertEqual(stored.format, "WEBP")
                self.assertLessEqual(max(stored.size), 1920)
        finally:
            media.image.delete(save=False)

    def test_resaving_without_changing_image_does_not_reprocess(self):
        media = Media.objects.create(
            titre="Test",
            type=Media.TYPE_PHOTO,
            image=self._uploaded_png(),
        )
        try:
            first_name = media.image.name
            media.titre = "Test modifie"
            media.save()
            media.refresh_from_db()
            self.assertEqual(media.image.name, first_name)
        finally:
            media.image.delete(save=False)
