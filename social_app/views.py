from django.shortcuts import render, redirect
import django
from .forms import ProfessionForm, CreateUserForm, LoginForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import *
from django.contrib.auth.decorators import *
# Create your views here.

def registerPage(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Account was created for {form.cleaned_data['username']}")
            return redirect('login')


    context = {
        'form': form,
    }

    return render(request, 'social_app/register.html', context)

def loginPage(request):
    form = LoginForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')
            
    context = {
        'form': form,
    }
    return render(request, 'social_app/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('home') 