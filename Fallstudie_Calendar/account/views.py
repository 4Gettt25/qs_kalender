# views.py
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.template import context

from .forms import RegisterForm, AccountAuthenticationForm
from django.contrib.auth.decorators import login_required


def loginView(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            print("User is authenticated")  # Debugging line
            login(request, user)
            print("User is logged in")  # Debugging line
            return redirect('home')
        else:
            print("User is not authenticated")  # Debugging line
    else:
        return render(request, 'login.html')

def registerView(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            username = form.cleaned_data.get('username')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/admin')
    else:
        form = RegisterForm()
    return render(request, 'login.html', {'form': form})


def logoutView(request):
    logout(request)
    return redirect('login')
