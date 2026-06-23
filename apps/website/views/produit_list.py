from django.shortcuts import render
from apps.website.models import Produit


CAT_LABELS = {
    Produit.CAT_PALME:      'Palme & dérivés',
    Produit.CAT_TROPICAL:   'Huiles tropicales',
    Produit.CAT_INDUSTRIEL: 'Industriels',
}


def produit_list(request):
    cat = request.GET.get('categorie', '')

    produits = Produit.objects.filter(actif=True).order_by('ordre')
    if cat in (Produit.CAT_PALME, Produit.CAT_TROPICAL, Produit.CAT_INDUSTRIEL):
        produits = produits.filter(categorie=cat)

    tous = Produit.objects.filter(actif=True).order_by('ordre')

    context = {
        'produits':       produits,
        'tous':           tous,
        'cat_active':     cat,
        'cat_labels':     CAT_LABELS,
        'categories':     Produit.CAT_CHOICES,
    }
    return render(request, 'pages/produit.html', context)
