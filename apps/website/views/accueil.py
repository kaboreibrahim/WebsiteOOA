from django.shortcuts import render
from apps.website.models.Hero import Hero
from apps.website.models.Produit import Produit
from apps.medias.models import Media


def accueil(request):
    heroes = Hero.objects.filter(actif=True)
    produits = Produit.objects.filter(actif=True)[:3]
    photos = Media.objects.filter(actif=True, type=Media.TYPE_PHOTO)[:4]
    videos = Media.objects.filter(actif=True, type=Media.TYPE_VIDEO)
    return render(request, 'pages/accueil.html', {
        'heroes': heroes,
        'produits': produits,
        'photos': photos,
        'videos': videos,
    })
