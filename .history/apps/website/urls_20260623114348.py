from django.urls import path
from django.views.generic import RedirectView
from .views import accueil

app_name = 'website'
urlpatterns = [
    path('', RedirectView.as_view(url='/accueil/'), name='accueil'),
    path('accueil/', accueil, name='accueil'),

]