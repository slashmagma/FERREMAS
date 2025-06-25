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
    path('',views.Home, name='Home2'),
    path('singup/',views.singup, name='singup'),
    path('logout/',views.signout, name='logout'),
    path('singin/',views.singin, name='singin'),
    path('Home/<str:nombre_cat>/Articulos/añadir/', views.crear_articulo, name='Agregarart'),
    path('Home/Categorias/<str:nombre_cat>/<str:nombre_art>/',views.detalle_Articulo, name='detalle_Articulos'),
    path('Home/Categorias/añadir/',views.crear_categoria, name='Agregarcat'),
    path('Home/Categorias/<str:nombre_cat>/',views.detalle_categoria, name='detalle_categorias'),
    path('Home/Categorias/<str:nombre_cat>/eliminar',views.eliminar_categoria, name='eliminar_cat'),
    path('Home/Categorias/<str:nombre_cat>/<str:nombre_art>/eliminar', views.eliminar_articulo, name='eliminar_art'),
    path('Home/Categorias/',views.lista_categoria, name='categorias'),
    path('Home/carrito',views.carrito, name='carrito'),
    path('añadir/<str:nombre_cat>/<str:nombre_art>/', views.añadir_carrito, name='Mas'),
    path('carrito/mas/<int:articulo_id>/', views.mas, name='mas'),
    path('carrito/limpiar/',views.limpiarcarrito, name='cln'),
    path('carrito/eliminar/<int:articulo_id>/',views.eliminar_artcarro, name='borrar'),
    path('carrito/restar/<int:articulo_id>/',views.restar_articulocarro, name='menos'),
    path('nosotros/', views.nosotros, name= 'nosotros'),
    path('Home/crear_cuenta/', views.crearcuenta, name='crearcuenta'),
    path('Home/Categorias/<str:nombre_cat>/<str:nombre_art>/restar', views.restar_Articulo, name='restar_art'),
    path('Home/Categorias/<str:nombre_cat>/<str:nombre_art>/añadir', views.añadir_articulo, name='añadir_art'),
    path('Perfil/', views.Perfil, name='Perfil'),
    path('webpay/', views.pagar_webpay, name='pagar_webpay'),
    path('webpay/retorno/', views.retorno, name='webpay_retorno'),
    path('Home/historial/', views.historial_compras, name='historial_compras'),
    path('guardar_direccion/', views.guardar_direccion, name='guardar_direccion'),
    path('eliminar/<int:articulo_id>/', views.eliminar_articulocarro, name='eliminar'),



  
    
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
