from django.urls import path, include
from .views import accueil

app_name = 'website'
urlpatterns = [
    path('', accueil, name='accueil'),
    
]