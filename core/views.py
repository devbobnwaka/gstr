from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, UserAuthenticationForm, UploadFileForm
from .gstr_pr_reco import reco_itr_2a

# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html', {})


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    form = UploadFileForm()
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        file_1 = request.FILES.get('file_1')
        file_2 = request.FILES.get('file_2')
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.file_1 = file_1
            instance.file_2 = file_2
            instance.save()
            print('hello', type(instance.file_1.url))
            result = reco_itr_2a(instance.file_1.url, instance.file_2.url)
            print(result)
            messages.success(request, "File Uploaded")
            return redirect("core:index")
        else:
            messages.error(request, "Upload failed")
    context = {"form": form}
    return render(request, "index.html", context)



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
	return redirect("core:home")

