from django.shortcuts import render 
from apps.Produit.models import Produit

def apropos(request):
    produits = Produit.objects.all()
    context = {
        'produits': produits
    }
    return render(request, 'pages/apropos.html', context)
