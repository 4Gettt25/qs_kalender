from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from account.forms import RegistrationForm, AccountAuthenticationForm

# View to handle user login
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

# View to handle user logout
def logoutView(request):
    logout(request)
    return redirect("login")

# View to handle user registration
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
