from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .Forms import CustomUserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .Forms import CategoriaForm, ArticuloForm
from .models import Categoria,articulo
from django.contrib.auth.decorators import login_required
from .Carrito import Carrito
from .Forms import CustomAuthenticationForm
import random 
import requests
#este es para poder personalizar el inicio de sesion de django
# Create your views here.





def Home(request):
    return render(request, 'Home.html', {
        
    })
def singup(request):
    if request.method == 'GET':
        return render(request, 'singup.html', {
           'form': CustomUserCreationForm(request_user=request.user)
        })
    else:
        form = CustomUserCreationForm(request.POST, request_user=request.user)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('Home')
            except:
                return render(request, 'singup.html', {
                    'form': CustomUserCreationForm(),
                    "error": 'El nombre de usuario ya existe'
                })
        else:
            return render(request, 'singup.html', {
                'form': form,
                "error": 'Las contraseñas no coinciden o el formulario no es válido'
            })
def crearcuenta(request):
    if request.method == 'GET':
        return render(request, 'creacion_cuentas.html', {
           'form': CustomUserCreationForm(request_user=request.user)
        })
    else:
        form = CustomUserCreationForm(request.POST, request_user=request.user)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                return redirect('Home')
            except:
                return render(request, 'creacion_cuentas.html', {
                    'form': CustomUserCreationForm(),
                    "error": 'El nombre de usuario ya existe'
                })
        else:
            return render(request, 'creacion_cuentas.html', {
                'form': form,
                "error": 'Las contraseñas no coinciden o el formulario no es válido'
            })
                     
@login_required          
def signout(request):
    logout(request)
    return redirect('Home')

def singin(request):
    if request.method == 'GET':
        return render(request, 'singin.html', {
            'form': CustomAuthenticationForm()
        })
    else:
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Home')
        else:
            return render(request, 'singin.html', {
                'form': form,
                'error': 'El usuario o la contraseña son incorrectos'
            })
@login_required
def crear_categoria(request):
    if request.method == 'GET':
        return render(request, 'Agregarcat.html', {
            'Form': CategoriaForm()
            })
    else:
        try:
            form = CategoriaForm(request.POST, request.FILES)
            N_catalogo = form.save(commit=False)
            N_catalogo.user = request.user
            N_catalogo.save()
            return redirect('Home')
        except ValueError:
            print("Errores del formulario:", form.errors)
            return render(request, 'Agregarcat.html', {
                'Form': form,
                'error': 'Error al crear la categoría'
            })
            
@login_required        
def crear_articulo(request, nombre_cat):
    if request.method == 'GET':
        return render(request, 'Agregarart.html', {
            'Form': ArticuloForm()
            })
    else:
        try:
            form = ArticuloForm(request.POST, request.FILES)
            N_articulo = form.save(commit=False)
            N_articulo.user = request.user
            categoria = Categoria.objects.get(nombrecat=nombre_cat)
            N_articulo.Tipo = categoria.nombrecat 
            N_articulo.save()
            return redirect('detalle_categorias', nombre_cat=nombre_cat)

        except ValueError:
            print("Errores del formulario:", form.errors)
            return render(request, 'Agregarcat.html', {
                'Form': form,
                'error': 'Error al crear el artículo'
            })
        except Categoria.DoesNotExist:
            return render(request, 'Agregarart.html', {
                'Form': form,
                'error': 'Categoría no encontrada'
            })

def lista_categoria(request):
    categorias=Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})

def detalle_categoria(request, nombre_cat):
    categoria = get_object_or_404(Categoria, nombrecat=nombre_cat)
    Articulos = articulo.objects.filter(Tipo=nombre_cat)
    return render(request, 'detalle_categorias.html', {
        'categoria': categoria,
        'Articulos': Articulos
    })

@login_required     
def eliminar_categoria(request, nombre_cat):
    categoria = get_object_or_404(Categoria,nombrecat=nombre_cat, user=request.user)
    if request.method == 'POST':
        categoria.delete()
        return redirect('categorias')


def detalle_Articulo (request, nombre_cat, nombre_art):
    articulo_obj = get_object_or_404(articulo, nombreart=nombre_art)

    return render(request, 'detalle_articulos.html', {
    'articulo': articulo_obj,
    'nombre_cat': nombre_cat
})

def restar_Articulo(request, nombre_cat, nombre_art):
    try:
        articulo_obj = articulo.objects.get(nombreart=nombre_art)
        # Aquí va tu lógica para restar o modificar
        # Por ejemplo:
        if articulo_obj.cantidad > 0:
            articulo_obj.cantidad -= 1
            articulo_obj.save()
        else:
            articulo_obj.delete()
        return redirect('detalle_Articulos', nombre_cat=nombre_cat, nombre_art=nombre_art)  # ← SIEMPRE devolver una respuesta
    except articulo.DoesNotExist:
        # Manejar el error si no se encuentra el artículo
        return redirect('detalle_categorias', nombre_cat=nombre_cat) 

def añadir_articulo(request, nombre_cat, nombre_art):
    try:
        articulo_obj = articulo.objects.get(nombreart=nombre_art)
        # Aquí va tu lógica para añadir o modificar
        # Por ejemplo:
        articulo_obj.cantidad += 1
        articulo_obj.save()
        return redirect('detalle_Articulos', nombre_cat=nombre_cat, nombre_art=nombre_art)  # ← SIEMPRE devolver una respuesta
    except articulo.DoesNotExist:
        # Manejar el error si no se encuentra el artículo
        return redirect('detalle_categorias', nombre_cat=nombre_cat)

@login_required
def eliminar_articulo(request, nombre_cat, nombre_art):
    Articulo = get_object_or_404(articulo, nombreart=nombre_art, user=request.user)
    if request.method == 'POST':
        Articulo.delete()
        return redirect('detalle_categorias', nombre_cat=nombre_cat)

def nosotros(request):
    return render(request, 'nosotros.html')

def Perfil(request):
    return render(request, 'Perfil.html')




def añadir_carrito(request, nombre_cat, nombre_art):
    carrito= Carrito(request)
    Articulo= articulo.objects.get(nombreart=nombre_art, user=request.user)
    carrito.agregar(Articulo)
    return redirect('detalle_categorias', nombre_cat=nombre_cat)

def mas(request, articulo_id):
    carrito = Carrito(request)
    art = articulo.objects.get(id=articulo_id, user=request.user)
    carrito.agregar(art)
    return redirect('carrito')

def eliminar_artcarro(request, articulo_id):
   carrito = Carrito(request)
   art = articulo.objects.get(id=articulo_id, user=request.user)
   carrito.eliminar(art)
   return redirect('carrito')

def limpiarcarrito(request):
    carrito = Carrito(request)
    carrito.limpiar_carrito()
    return redirect('carrito')

def restar_articulocarro(request, articulo_id):
    carrito = Carrito(request)
    art = articulo.objects.get(id=articulo_id, user=request.user)
    carrito.eliminar_producto(art)
    return redirect('carrito')

def carrito(request):
    carrito_data = request.session.get('carrito', {})
    total = 0

    for key, item in carrito_data.items():
        total += Decimal(item['acumulado']) * item['cantidad']
        try:
            Articulo = get_object_or_404(articulo,nombreart=item['nombreart'])
            item['nombre_art'] = Articulo.nombreart 
        except articulo.DoesNotExist:
            item['nombre_art'] = 'categoria no encontrada'  

    return render(request, 'carrito.html', {
        'Carrito': carrito_data,
        'total_factura': total
    })
    
def pagar_webpay(request):
    total = request.GET.get('monto', 15000)
    buy_order = str(random.randint(10000, 99999))
    session_id = str(random.randint(10000, 99999))
    return_url = request.build_absolute_uri('/webpay/retorno/')

    headers = {
        "Tbk-Api-Key-Id": "597055555532",
        "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        "Content-Type": "application/json"
    }
    payload = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": int(total),
        "return_url": return_url
    }

    response = requests.post(
        "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.0/transactions",
        json=payload,
        headers=headers
    )
    data = response.json()

    return render(request, "webpay.html", {
        "token": data.get("token"),
        "url_tbk": data.get("url"),
        "submit": "Pagar ahora"
    })