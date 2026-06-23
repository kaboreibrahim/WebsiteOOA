from django.urls import path
from django.views.generic import RedirectView
from .views import accueil, produit_detail, produit_list, contact, apropos

app_name = 'website'
urlpatterns = [
    path('', RedirectView.as_view(url='/accueil/'), name='accueil'),
    path('accueil/', accueil, name='accueil'),
    path('a-propos/', apropos, name='apropos'),
    path('contact/', contact, name='contact'),
]
