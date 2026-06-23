from django.contrib import admin
from .models import Hero, Produit, Contact, Personne, Partenaire


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('titre', 'actif', 'ordre')
    list_editable = ('actif', 'ordre')
    list_filter = ('actif',)
    search_fields = ('titre', 'description')


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display  = ('nom', 'categorie', 'conditionnement', 'origine', 'lead_time', 'actif', 'ordre')
    list_editable = ('categorie', 'actif', 'ordre')
    list_filter   = ('categorie', 'actif')
    search_fields = ('nom', 'description', 'origine')
    fieldsets = (
        (None, {'fields': ('nom', 'categorie', 'description', 'image', 'actif', 'ordre')}),
        ('Spécifications techniques', {'fields': ('ffa', 'iv', 'point_fusion', 'conditionnement', 'origine', 'lead_time', 'usage')}),
    )


@admin.register(Personne)
class PersonneAdmin(admin.ModelAdmin):
    list_display  = ('nom', 'profession', 'mail', 'role', 'departement', 'ordre', 'actif')
    list_editable = ('role', 'departement', 'ordre', 'actif')
    list_filter   = ('role', 'departement', 'actif')
    search_fields = ('nom', 'profession', 'mail')


@admin.register(Partenaire)
class PartenaireAdmin(admin.ModelAdmin):
    list_display  = ('nom', 'lien', 'ordre', 'actif')
    list_editable = ('ordre', 'actif')
    list_filter   = ('actif',)
    search_fields = ('nom',)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'sujet', 'date_envoi', 'lu')
    list_editable = ('lu',)
    list_filter = ('sujet', 'lu')
    search_fields = ('nom', 'email', 'message')
    readonly_fields = ('nom', 'email', 'sujet', 'message', 'date_envoi')
