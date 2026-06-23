from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog/',        views.blog_list,   name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
]
