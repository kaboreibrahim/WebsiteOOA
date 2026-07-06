from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages as flash
from django.shortcuts import render, redirect, get_object_or_404
from apps.website.models import Produit, Contact, Personne, Partenaire, Hero
from apps.blog.models import Article, Categorie
from apps.medias.models import Media
from .forms import (
    HeroForm, ProduitForm, CategorieForm, ArticleForm,
    MediaForm, PersonneForm, PartenaireForm,
)


# ── DASHBOARD ────────────────────────────────────────────────────────────────

@staff_member_required
def dashboard(request):
    context = {
        'active_section': 'dashboard',
        'produits_total': Produit.objects.count(),
        'produits_actifs': Produit.objects.filter(actif=True).count(),
        'articles_total': Article.objects.count(),
        'articles_publies': Article.objects.filter(actif=True).count(),
        'articles_une': Article.objects.filter(en_une=True, actif=True).count(),
        'categories_total': Categorie.objects.count(),
        'medias_total': Media.objects.count(),
        'medias_photos': Media.objects.filter(type=Media.TYPE_PHOTO).count(),
        'medias_videos': Media.objects.filter(type=Media.TYPE_VIDEO).count(),
        'contacts_total': Contact.objects.count(),
        'contacts_non_lus': Contact.objects.filter(lu=False).count(),
        'contacts_recents': Contact.objects.order_by('-date_envoi')[:8],
        'personnel_total': Personne.objects.count(),
        'dirigeants_total': Personne.objects.filter(role=Personne.Role.DIRIGEANT).count(),
        'partenaires_total': Partenaire.objects.count(),
        'partenaires_actifs': Partenaire.objects.filter(actif=True).count(),
        'heroes_total': Hero.objects.count(),
        'heroes_actifs': Hero.objects.filter(actif=True).count(),
        'articles_recents': Article.objects.order_by('-date_publication')[:5],
    }
    return render(request, 'dashboard/dashboard.html', context)


# ── HEROES ───────────────────────────────────────────────────────────────────

@staff_member_required
def heroes_list(request):
    return render(request, 'dashboard/heroes/list.html', {
        'heroes': Hero.objects.all(),
        'active_section': 'heroes',
    })


@staff_member_required
def heroes_form(request, pk=None):
    obj = get_object_or_404(Hero, pk=pk) if pk else None
    if request.method == 'POST':
        form = HeroForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Banner hero sauvegardé.')
            return redirect('dashboard:heroes_list')
    else:
        form = HeroForm(instance=obj)
    return render(request, 'dashboard/_form.html', {
        'form': form, 'obj': obj,
        'section_title': 'Heroes', 'section_url': 'dashboard:heroes_list',
        'item_name': 'Banner hero', 'active_section': 'heroes',
    })


@staff_member_required
def heroes_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Hero, pk=pk).delete()
        flash.success(request, 'Banner hero supprimé.')
    return redirect('dashboard:heroes_list')


# ── PRODUITS ─────────────────────────────────────────────────────────────────

@staff_member_required
def produits_list(request):
    qs = Produit.objects.all()
    cat = request.GET.get('cat', '')
    if cat:
        qs = qs.filter(categorie=cat)
    return render(request, 'dashboard/produits/list.html', {
        'produits': qs,
        'active_section': 'produits',
        'cat_filter': cat,
        'cat_choices': Produit.CAT_CHOICES,
    })


@staff_member_required
def produits_form(request, pk=None):
    obj = get_object_or_404(Produit, pk=pk) if pk else None
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Produit sauvegardé.')
            return redirect('dashboard:produits_list')
    else:
        form = ProduitForm(instance=obj)
    return render(request, 'dashboard/_form.html', {
        'form': form, 'obj': obj,
        'section_title': 'Produits', 'section_url': 'dashboard:produits_list',
        'item_name': 'Produit', 'active_section': 'produits',
    })


@staff_member_required
def produits_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Produit, pk=pk).delete()
        flash.success(request, 'Produit supprimé.')
    return redirect('dashboard:produits_list')


# ── ARTICLES ─────────────────────────────────────────────────────────────────

@staff_member_required
def articles_list(request):
    qs = Article.objects.select_related('categorie').all()
    statut = request.GET.get('statut', '')
    if statut == 'publie':
        qs = qs.filter(actif=True)
    elif statut == 'brouillon':
        qs = qs.filter(actif=False)
    elif statut == 'une':
        qs = qs.filter(en_une=True)
    return render(request, 'dashboard/articles/list.html', {
        'articles': qs,
        'active_section': 'articles',
        'statut_filter': statut,
    })


@staff_member_required
def articles_form(request, pk=None):
    obj = get_object_or_404(Article, pk=pk) if pk else None
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Article sauvegardé.')
            return redirect('dashboard:articles_list')
    else:
        form = ArticleForm(instance=obj)
        if obj and obj.date_publication:
            form.initial['date_publication'] = obj.date_publication.strftime('%Y-%m-%d')
    return render(request, 'dashboard/_form.html', {
        'form': form, 'obj': obj,
        'section_title': 'Articles', 'section_url': 'dashboard:articles_list',
        'item_name': 'Article', 'active_section': 'articles',
    })


@staff_member_required
def articles_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Article, pk=pk).delete()
        flash.success(request, 'Article supprimé.')
    return redirect('dashboard:articles_list')


# ── CATÉGORIES ────────────────────────────────────────────────────────────────

@staff_member_required
def categories_list(request):
    categories = Categorie.objects.all()
    return render(request, 'dashboard/categories/list.html', {
        'categories': categories,
        'active_section': 'categories',
    })


@staff_member_required
def categories_form(request, pk=None):
    obj = get_object_or_404(Categorie, pk=pk) if pk else None
    if request.method == 'POST':
        form = CategorieForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Catégorie sauvegardée.')
            return redirect('dashboard:categories_list')
    else:
        form = CategorieForm(instance=obj)
    return render(request, 'dashboard/_form.html', {
        'form': form, 'obj': obj,
        'section_title': 'Catégories', 'section_url': 'dashboard:categories_list',
        'item_name': 'Catégorie', 'active_section': 'categories',
    })


@staff_member_required
def categories_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Categorie, pk=pk).delete()
        flash.success(request, 'Catégorie supprimée.')
    return redirect('dashboard:categories_list')


# ── MÉDIAS ────────────────────────────────────────────────────────────────────

@staff_member_required
def medias_list(request):
    qs = Media.objects.all()
    type_filter = request.GET.get('type', '')
    if type_filter:
        qs = qs.filter(type=type_filter)
    return render(request, 'dashboard/medias/list.html', {
        'medias': qs,
        'active_section': 'medias',
        'type_filter': type_filter,
    })


@staff_member_required
def medias_form(request, pk=None):
    obj = get_object_or_404(Media, pk=pk) if pk else None
    if request.method == 'POST':
        form = MediaForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Média sauvegardé.')
            return redirect('dashboard:medias_list')
    else:
        form = MediaForm(instance=obj)
    return render(request, 'dashboard/_form.html', {
        'form': form, 'obj': obj,
        'section_title': 'Médias', 'section_url': 'dashboard:medias_list',
        'item_name': 'Média', 'active_section': 'medias',
    })


@staff_member_required
def medias_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Media, pk=pk).delete()
        flash.success(request, 'Média supprimé.')
    return redirect('dashboard:medias_list')


# ── MESSAGES ─────────────────────────────────────────────────────────────────

@staff_member_required
def messages_list(request):
    qs = Contact.objects.all()
    lu_filter = request.GET.get('lu', '')
    if lu_filter == '0':
        qs = qs.filter(lu=False)
    elif lu_filter == '1':
        qs = qs.filter(lu=True)
    return render(request, 'dashboard/messages/list.html', {
        'messages_list': qs,
        'active_section': 'messages',
        'lu_filter': lu_filter,
        'non_lus': Contact.objects.filter(lu=False).count(),
    })


@staff_member_required
def messages_detail(request, pk):
    msg = get_object_or_404(Contact, pk=pk)
    if not msg.lu:
        msg.lu = True
        msg.save(update_fields=['lu'])
    return render(request, 'dashboard/messages/detail.html', {
        'msg': msg,
        'active_section': 'messages',
    })


@staff_member_required
def messages_toggle_lu(request, pk):
    if request.method == 'POST':
        msg = get_object_or_404(Contact, pk=pk)
        msg.lu = not msg.lu
        msg.save(update_fields=['lu'])
    return redirect('dashboard:messages_list')


@staff_member_required
def messages_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Contact, pk=pk).delete()
        flash.success(request, 'Message supprimé.')
    return redirect('dashboard:messages_list')


# ── PERSONNEL ─────────────────────────────────────────────────────────────────

@staff_member_required
def personnel_list(request):
    return render(request, 'dashboard/personnel/list.html', {
        'personnel': Personne.objects.all(),
        'active_section': 'personnel',
    })


@staff_member_required
def personnel_form(request, pk=None):
    obj = get_object_or_404(Personne, pk=pk) if pk else None
    if request.method == 'POST':
        form = PersonneForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Personne sauvegardée.')
            return redirect('dashboard:personnel_list')
    else:
        form = PersonneForm(instance=obj)
    return render(request, 'dashboard/_form.html', {
        'form': form, 'obj': obj,
        'section_title': 'Personnel', 'section_url': 'dashboard:personnel_list',
        'item_name': 'Personne', 'active_section': 'personnel',
    })


@staff_member_required
def personnel_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Personne, pk=pk).delete()
        flash.success(request, 'Personne supprimée.')
    return redirect('dashboard:personnel_list')


# ── PARTENAIRES ───────────────────────────────────────────────────────────────

@staff_member_required
def partenaires_list(request):
    return render(request, 'dashboard/partenaires/list.html', {
        'partenaires': Partenaire.objects.all(),
        'active_section': 'partenaires',
    })


@staff_member_required
def partenaires_form(request, pk=None):
    obj = get_object_or_404(Partenaire, pk=pk) if pk else None
    if request.method == 'POST':
        form = PartenaireForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            flash.success(request, 'Partenaire sauvegardé.')
            return redirect('dashboard:partenaires_list')
    else:
        form = PartenaireForm(instance=obj)
    return render(request, 'dashboard/_form.html', {
        'form': form, 'obj': obj,
        'section_title': 'Partenaires', 'section_url': 'dashboard:partenaires_list',
        'item_name': 'Partenaire', 'active_section': 'partenaires',
    })


@staff_member_required
def partenaires_delete(request, pk):
    if request.method == 'POST':
        get_object_or_404(Partenaire, pk=pk).delete()
        flash.success(request, 'Partenaire supprimé.')
    return redirect('dashboard:partenaires_list')
