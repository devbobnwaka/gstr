from django.urls import path
from . import views

app_name='core'
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path("logout", views.logout_view, name= "logout"),
]
