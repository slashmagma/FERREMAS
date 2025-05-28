from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from .Forms import CategoriaForm, ArticuloForm
from .models import Categoria,articulo
from django.contrib.auth.decorators import login_required
from .Carrito import Carrito
# Create your views here.
def Home(request):
    return render(request, 'Home.html', {
        
    })
def singup(request):

    if request.method == 'GET':
        return render(request, 'singup.html', {
        'form': UserCreationForm()
        })
        
    else:
        if request.POST['password1'] == request.POST['password2']:
        #registra usario
            try:
                user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password1'],)
                user.save()
                login(request, user)
                return  redirect('Home')
            except:
              return render(request, 'singup.html', {
                'form': UserCreationForm(),
                "error": 'El nombre de usuario ya existe'
                })
        return render(request, 'singup.html', {
                'form': UserCreationForm(),
                    "error": 'El pasword no coincide'
                    })
            
@login_required          
def signout(request):
    logout(request)
    return redirect('singup')

def singin(request):
    if request.method == 'GET':
        return render(request, 'singin.html',{
            'form': AuthenticationForm
        })
    
    else:
        user = authenticate(request, username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'singin.html', {
              'form': AuthenticationForm
                , 'error': 'El usuario o la contraseña son incorrectos'
                })
        else: 
            login(request, user)
            return redirect('Home')
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
@login_required
def lista_categoria(request):
    categorias=Categoria.objects.all()
    return render(request, 'categorias.html', {'categorias': categorias})
@login_required
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

@login_required
def detalle_Articulo (request, nombre_cat, nombre_art):
    Articulo = get_object_or_404(articulo, nombreart=nombre_art, user=request.user)
    return render(request, 'detalle_articulos.html', {
        'Articulo': Articulo,
        'nombre_cat': nombre_cat
    })
@login_required
def eliminar_articulo(request, nombre_cat, nombre_art):
    Articulo = get_object_or_404(articulo, nombreart=nombre_art, user=request.user)
    if request.method == 'POST':
        Articulo.delete()
        return redirect('detalle_categorias', nombre_cat=nombre_cat)



def añadir_carrito(request, nombre_cat, nombre_art,articulo_nom):
    carrito= Carrito(request)
    Articulo= articulo.objects.get(nombreart=articulo_nom, user=request.user)
    carrito.agregar(Articulo)
    return redirect('detalle_categorias', nombre_cat=nombre_cat)


def eliminar_carrito(request, articulo_nom):
   carrito = Carrito(request)
   Articulo = articulo.objects.get(nombreart = articulo_nom, user=request.user)
   carrito.eliminar(Articulo)
   return redirect('carrito')

def limpiarcarrito(request):
    carrito = Carrito(request)
    carrito.limpiar_carrito()
    return redirect('carrito')

def restar_articulo(request, nombre_cat, nombre_art):
    carrito = Carrito(request)
    Articulo = articulo.objects.get(nombreart=nombre_art, user=request.user)
    carrito.eliminar_producto(Articulo)
    return redirect('detalle_categorias', nombre_cat=nombre_cat)

def carrito(request):
    carrito_data = request.session.get('carrito', {})
    total = 0

    for key, item in carrito_data.items():
        total += Decimal(item['valorunidad']) * item['cantidad']
        try:
            Articulo = get_object_or_404(articulo,nombreart=item['nombreart'])
            item['nombre_art'] = Articulo.nombreart 
        except articulo.DoesNotExist:
            item['nombre_art'] = 'categoria no encontrada'  

    return render(request, 'carrito.html', {
        'Carrito': carrito_data,
        'total_factura': total
    })