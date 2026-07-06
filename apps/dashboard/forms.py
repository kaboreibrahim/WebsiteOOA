from django import forms
from apps.website.models import Hero, Produit, Personne, Partenaire
from apps.blog.models import Article, Categorie
from apps.medias.models import Media

_INPUT = (
    'w-full rounded-xl border border-gray-200 dark:border-[#2d3d30] '
    'bg-white dark:bg-[#111814] text-gray-900 dark:text-gray-100 '
    'px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#004d1e] '
    'focus:border-transparent transition-colors placeholder-gray-400 dark:placeholder-gray-600'
)
_SELECT = (
    'w-full rounded-xl border border-gray-200 dark:border-[#2d3d30] '
    'bg-white dark:bg-[#111814] text-gray-900 dark:text-gray-100 '
    'px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#004d1e] transition-colors'
)
_TEXTAREA = (
    'w-full rounded-xl border border-gray-200 dark:border-[#2d3d30] '
    'bg-white dark:bg-[#111814] text-gray-900 dark:text-gray-100 '
    'px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#004d1e] '
    'focus:border-transparent transition-colors resize-none placeholder-gray-400 dark:placeholder-gray-600'
)
_CHECKBOX = 'w-5 h-5 rounded border-gray-300 dark:border-gray-600 text-[#004d1e] focus:ring-[#004d1e] cursor-pointer'
_FILE = (
    'block w-full text-sm text-gray-500 dark:text-gray-400 cursor-pointer '
    'file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 '
    'file:text-sm file:font-semibold file:bg-[#004d1e] file:text-white '
    'hover:file:bg-[#003d17] transition-colors'
)


class DashboardMixin:
    def _style(self):
        for field in self.fields.values():
            w = field.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs.update({'class': _CHECKBOX, 'is_checkbox': True})
            elif isinstance(w, forms.Textarea):
                w.attrs.update({'class': _TEXTAREA, 'rows': 5, 'full_width': True})
            elif isinstance(w, forms.Select):
                w.attrs.update({'class': _SELECT})
            elif isinstance(w, (forms.ClearableFileInput, forms.FileInput)):
                w.attrs.update({'class': _FILE, 'full_width': True, 'is_file': True})
            else:
                w.attrs.update({'class': _INPUT})


class HeroForm(DashboardMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    class Meta:
        model = Hero
        fields = ['titre', 'description', 'image', 'actif', 'ordre']


class ProduitForm(DashboardMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    class Meta:
        model = Produit
        fields = [
            'nom', 'categorie', 'actif', 'ordre',
            'description', 'image',
            'ffa', 'iv', 'point_fusion',
            'conditionnement', 'origine', 'lead_time', 'usage',
        ]


class CategorieForm(DashboardMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    class Meta:
        model = Categorie
        fields = ['nom']


class ArticleForm(DashboardMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()
        self.fields['date_publication'].widget = forms.DateInput(
            attrs={'type': 'date', 'class': _INPUT},
            format='%Y-%m-%d',
        )
        self.fields['contenu'].widget.attrs['rows'] = 12

    class Meta:
        model = Article
        fields = [
            'titre', 'categorie', 'auteur', 'date_publication', 'temps_lecture',
            'en_une', 'actif',
            'extrait', 'image_hero', 'contenu',
        ]


class MediaForm(DashboardMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    class Meta:
        model = Media
        fields = [
            'type', 'categorie', 'titre', 'actif', 'ordre', 'en_vedette',
            'description', 'image', 'vignette', 'video_url',
        ]


class PersonneForm(DashboardMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    class Meta:
        model = Personne
        fields = ['nom', 'profession', 'mail', 'role', 'departement', 'icone', 'ordre', 'actif', 'photo']


class PartenaireForm(DashboardMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style()

    class Meta:
        model = Partenaire
        fields = ['nom', 'lien', 'ordre', 'actif', 'logo']
