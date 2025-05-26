from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate


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
                'form': UserCreationForm,
                "error": 'El nombre de usuario ya existe'
                })
        return render(request, 'singup.html', {
                'form': UserCreationForm,
                    "error": 'El pasword no coincide'
                    })
            
            
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
            return redirect('Home')
def crearcategoria(request):
    return render(request, 'Agregarcat.html')

def nosotros(request):
    return render(request, 'nosotros.html')


   
     