from django.shortcuts import render
from apps.produit.models import Produit

def apropos(request):
    produits = Produit.objects.all()
    context = {
        'produits': produits
    }
    return render(request, 'pages/apropos.html', context)
