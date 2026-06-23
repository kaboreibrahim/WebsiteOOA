from django.shortcuts import render
from .models import Media


def medias_list(request):
    filtre = request.GET.get('filtre', '')

    medias = Media.objects.filter(actif=True)

    if filtre == 'photos':
        medias = medias.filter(type=Media.TYPE_PHOTO)
    elif filtre == 'videos':
        medias = medias.filter(type=Media.TYPE_VIDEO)
    elif filtre in [Media.CAT_OPERATIONS, Media.CAT_PRODUITS, Media.CAT_SOURCING, Media.CAT_LOGISTIQUE]:
        medias = medias.filter(categorie=filtre)

    en_vedette = Media.objects.filter(actif=True, type=Media.TYPE_VIDEO, en_vedette=True).first()
    grille     = medias.exclude(pk=en_vedette.pk) if en_vedette else medias

    context = {
        'medias':     grille,
        'en_vedette': en_vedette,
        'filtre':     filtre,
        'categories': Media.CAT_CHOICES,
    }
    return render(request, 'pages/media.html', context)
