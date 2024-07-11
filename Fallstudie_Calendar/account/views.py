from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from account.forms import RegistrationForm, AccountAuthenticationForm
from django.views.generic import TemplateView

# Create your views here.

def loginView(request):
    context = {}
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = AccountAuthenticationForm()
    context['form'] = form
    return render(request, "login.html", context)

def logoutView(request):
    logout(request)
    return redirect("login")

def registerView(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    context['form'] = form
    return render(request, "registrieren.html", context)

def home(request):
    return render(request, 'account/home.html')

class HomeView(TemplateView):
    template_name = 'home.html'