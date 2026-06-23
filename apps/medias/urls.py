from django.urls import path
from .views import medias_list

app_name = 'medias'
urlpatterns = [
    path('medias/', medias_list, name='medias_list'),
]
