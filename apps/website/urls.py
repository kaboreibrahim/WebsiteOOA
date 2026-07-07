from django.urls import path
from django.views.generic import RedirectView
from .views import accueil, produit_detail, produit_list, contact, apropos, flexitank, isotank, sourcing

app_name = 'website'
urlpatterns = [
    path('', RedirectView.as_view(url='/accueil/')),
    path('accueil/', accueil, name='accueil'),
    path('apropos/', apropos, name='apropos'),
    path('contact/', contact, name='contact'),
    path('produits/', produit_list, name='produit_list'),
    path('produits/<uuid:pk>/', produit_detail, name='produit_detail'),
    path('logistique/flexitank/', flexitank, name='flexitank'),
    path('logistique/isotank/', isotank, name='isotank'),
    path('sourcing/', sourcing, name='sourcing'),
]
