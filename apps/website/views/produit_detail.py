from django.shortcuts import render, get_object_or_404
from apps.website.models import Produit


def produit_detail(request, pk):
    produit = get_object_or_404(Produit, pk=pk, actif=True)
    similaires = Produit.objects.filter(actif=True, categorie=produit.categorie).exclude(pk=pk).order_by('ordre')[:4]

    context = {
        'produit':    produit,
        'similaires': similaires,
    }
    return render(request, 'pages/produit_detail.html', context)
