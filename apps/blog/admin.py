from django.contrib import admin
from .models import Categorie, Article


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display  = ('nom', 'slug')
    prepopulated_fields = {'slug': ('nom',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display        = ('titre', 'categorie', 'auteur', 'date_publication', 'en_une', 'actif')
    list_editable       = ('en_une', 'actif')
    list_filter         = ('actif', 'en_une', 'categorie')
    search_fields       = ('titre', 'extrait', 'contenu', 'auteur')
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy      = 'date_publication'
