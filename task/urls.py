from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('singup/', views.singup, name= 'singup'),
    path('signout/', views.signout, name= 'signout'),
    path('singin/', views.singin, name= 'singin'),
    path('crearcategoria/', views.crearcategoria, name= 'crearcategoria'),
    path('nosotros/', views.nosotros, name= 'nosotros'),
]