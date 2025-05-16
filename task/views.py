from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login


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
            
        return HttpResponse('password no coinciden')
    
    


   
     