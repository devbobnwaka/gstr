import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, HttpResponse, FileResponse, Http404
from django.contrib.auth.decorators import login_required

from .forms import UserCreationForm, UserAuthenticationForm, UploadFileForm
from .gstr_pr_reco import reco_itr_2a

# Create your views here.
def home(request: HttpRequest) -> HttpResponse:
    return render(request, 'home.html', {})


@login_required()
def index(request: HttpRequest, is_file_path_ready=None) -> HttpResponse:
    is_upload = False
    file_path_1=None
    file_path_2=None
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
            is_upload=True
            file_path_1=instance.file_1.path
            file_path_2=instance.file_2.path
            messages.success(request, "File Uploaded")
            # print('hello', type(instance.file_1.url))
            # print(os.path.join(settings.BASE_DIR, instance.file_1.name.replace("/", os.path.sep)))
            # print(instance.file_1.path)
            # result = reco_itr_2a(instance.file_1.path, instance.file_2.path)
            # file_full_path = result.get('fullpath2')
            # print(file_full_path)
            # is_file_path_ready = file_full_path
            # return redirect("core:index")
        else:
            messages.error(request, "Upload failed, File is not a valid file!!!")
    context = {"form": form,
                "is_file_path_ready":is_file_path_ready,
                "is_upload":is_upload,
                "file_path_1":file_path_1,
                "file_path_2":file_path_2
                }
    return render(request, "index.html", context)


@login_required()
def reconcile(request, file_1, file_2):
    if file_1 and file_2:
        try:
            result = reco_itr_2a(file_1, file_2)
            file_full_path = result.get('fullpath2')
            is_file_path_ready = file_full_path
            messages.success(request, "Reconcile done!!!")
            return redirect('core:index_with_path', is_file_path_ready=is_file_path_ready)
        except:
            messages.error(request, "Something went wrong while reconciling!!!")
            return redirect('core:index')
    messages.error(request, "File field is invalid!!!")
    return redirect('core:index')


@login_required()
def download_file(request, file_full_path):
    # file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    print(file_full_path)
    if os.path.exists(file_full_path):
        with open(file_full_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_full_path)
            return response
    raise Http404


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

