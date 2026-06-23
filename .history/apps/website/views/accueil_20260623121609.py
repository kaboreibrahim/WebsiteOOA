from django.shortcuts import render
from apps.website.models import Hero


def accueil(request):
    hero = Hero.objects.filter(actif=True).first()
    return render(request, 'pages/accueil.html', {'hero': hero})
