from django.shortcuts import render, get_object_or_404
from .models import Article, Categorie


def blog_list(request):
    cat_slug = request.GET.get('categorie', '')
    q        = request.GET.get('q', '').strip()

    articles = Article.objects.filter(actif=True)

    if cat_slug:
        articles = articles.filter(categorie__slug=cat_slug)
    if q:
        articles = articles.filter(titre__icontains=q) | articles.filter(extrait__icontains=q)

    en_une     = Article.objects.filter(actif=True, en_une=True).first()
    categories = Categorie.objects.all()
    recents    = Article.objects.filter(actif=True).exclude(en_une=True)[:3]

    context = {
        'articles':   articles,
        'en_une':     en_une,
        'categories': categories,
        'recents':    recents,
        'cat_slug':   cat_slug,
        'q':          q,
    }
    return render(request, 'pages/blog.html', context)


def blog_detail(request, slug):
    article   = get_object_or_404(Article, slug=slug, actif=True)
    similaires = Article.objects.filter(actif=True, categorie=article.categorie).exclude(pk=article.pk)[:3]

    context = {
        'article':   article,
        'similaires': similaires,
    }
    return render(request, 'pages/blog_detail.html', context)
