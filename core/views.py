from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, UserAuthenticationForm

# Create your views here.
@login_required
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html', {})


def register(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('core:home')
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("core:home")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    context={
        "form":form
    }
    return render(request, 'accounts/register.html', context)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect('core:home')
    if request.method == "POST":
        form = UserAuthenticationForm(request.POST)
        email   = request.POST.get('email')
        password = request.POST.get('password')
        user =  authenticate(email=email, password=password)
        if user:
            login(request, user)
            messages.success(request, f"You are now logged in as {email}.")
            return redirect("core:home")
        else:
            messages.error(request,"Invalid username or password.")
    form = UserAuthenticationForm()
    context={
        "form":form
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout_view(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("core:login")

