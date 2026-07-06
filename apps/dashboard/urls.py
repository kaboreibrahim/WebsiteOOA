from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),

    # Heroes
    path('dashboard/heroes/', views.heroes_list, name='heroes_list'),
    path('dashboard/heroes/add/', views.heroes_form, name='heroes_add'),
    path('dashboard/heroes/<int:pk>/edit/', views.heroes_form, name='heroes_edit'),
    path('dashboard/heroes/<int:pk>/delete/', views.heroes_delete, name='heroes_delete'),

    # Produits
    path('dashboard/produits/', views.produits_list, name='produits_list'),
    path('dashboard/produits/add/', views.produits_form, name='produits_add'),
    path('dashboard/produits/<int:pk>/edit/', views.produits_form, name='produits_edit'),
    path('dashboard/produits/<int:pk>/delete/', views.produits_delete, name='produits_delete'),

    # Articles
    path('dashboard/articles/', views.articles_list, name='articles_list'),
    path('dashboard/articles/add/', views.articles_form, name='articles_add'),
    path('dashboard/articles/<int:pk>/edit/', views.articles_form, name='articles_edit'),
    path('dashboard/articles/<int:pk>/delete/', views.articles_delete, name='articles_delete'),

    # Catégories
    path('dashboard/categories/', views.categories_list, name='categories_list'),
    path('dashboard/categories/add/', views.categories_form, name='categories_add'),
    path('dashboard/categories/<int:pk>/edit/', views.categories_form, name='categories_edit'),
    path('dashboard/categories/<int:pk>/delete/', views.categories_delete, name='categories_delete'),

    # Médias
    path('dashboard/medias/', views.medias_list, name='medias_list'),
    path('dashboard/medias/add/', views.medias_form, name='medias_add'),
    path('dashboard/medias/<int:pk>/edit/', views.medias_form, name='medias_edit'),
    path('dashboard/medias/<int:pk>/delete/', views.medias_delete, name='medias_delete'),

    # Messages
    path('dashboard/messages/', views.messages_list, name='messages_list'),
    path('dashboard/messages/<int:pk>/', views.messages_detail, name='messages_detail'),
    path('dashboard/messages/<int:pk>/toggle-lu/', views.messages_toggle_lu, name='messages_toggle_lu'),
    path('dashboard/messages/<int:pk>/delete/', views.messages_delete, name='messages_delete'),

    # Personnel
    path('dashboard/personnel/', views.personnel_list, name='personnel_list'),
    path('dashboard/personnel/add/', views.personnel_form, name='personnel_add'),
    path('dashboard/personnel/<int:pk>/edit/', views.personnel_form, name='personnel_edit'),
    path('dashboard/personnel/<int:pk>/delete/', views.personnel_delete, name='personnel_delete'),

    # Partenaires
    path('dashboard/partenaires/', views.partenaires_list, name='partenaires_list'),
    path('dashboard/partenaires/add/', views.partenaires_form, name='partenaires_add'),
    path('dashboard/partenaires/<int:pk>/edit/', views.partenaires_form, name='partenaires_edit'),
    path('dashboard/partenaires/<int:pk>/delete/', views.partenaires_delete, name='partenaires_delete'),
]
