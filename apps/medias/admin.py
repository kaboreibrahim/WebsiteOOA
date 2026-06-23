from django.contrib import admin
from .models import Media


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display  = ('titre', 'type', 'categorie', 'en_vedette', 'actif', 'ordre')
    list_editable = ('type', 'categorie', 'en_vedette', 'actif', 'ordre')
    list_filter   = ('type', 'categorie', 'actif', 'en_vedette')
    search_fields = ('titre', 'description')
