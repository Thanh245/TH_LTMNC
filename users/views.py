from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, get_user_model, logout
from django.contrib.auth import login as auth_login
from .forms import RegisterForm
from .models import *


def register(request):
    next = request.GET.get('next')
    form = RegisterForm(request.POST or None)


    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        print("ok")
        # new_user = authenticate(username=user.username, password=password)
        # login(request, new_user)
        if next:
            return redirect(next)
        return redirect('/')

    context = {
        'form': form,
    }

    return render(request, "users/register.html", context)

def sign_out(request):
    logout(request)
    return redirect('/')

def login(request):
    message = ''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            message = 'Login failed'

    return render(request, 'users/login.html', {'message': message})

