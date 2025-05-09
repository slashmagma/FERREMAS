from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse


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
                return  HttpResponse('usuario creado')
            except:
                return HttpResponse('usuario ya existe')
        return HttpResponse('password no coinciden')


   
     