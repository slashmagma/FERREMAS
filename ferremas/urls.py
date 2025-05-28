"""
URL configuration for ferremas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Home/',views.Home, name='Home'),
    path('',views.singin, name='singin2'),
    path('singup/',views.singup, name='singup'),
    path('logout/',views.signout, name='logout'),
    path('singin/',views.singin, name='singin'),
    path('<str:nombre_cat>/Articulos/añadir/', views.crear_articulo, name='Agregarart'),
    path('Categorias/<str:nombre_cat>/<str:nombre_art>/',views.detalle_Articulo, name='detalle_Articulos'),
    path('Categorias/añadir/',views.crear_categoria, name='Agregarcat'),
    path('Categorias/<str:nombre_cat>/',views.detalle_categoria, name='detalle_categorias'),
    path('Categorias/<str:nombre_cat>/eliminar',views.eliminar_categoria, name='eliminar_cat'),
    path('Categorias/<str:nombre_cat>/<str:nombre_art>/eliminar', views.eliminar_articulo, name='eliminar_art'),
    path('Categorias/',views.lista_categoria, name='categorias'),
    path('Home/carrito',views.carrito, name='carrito'),
    path('añadir/<str:nombre_cat>/<str:nombre_art>/', views.añadir_carrito, name='mas'),
    path('eliminar/',views.eliminar_carrito, name='cln'),
    path('restar/<str:articulo_nom>',views.restar_articulo, name='menos'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)