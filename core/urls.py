from django.urls import path
from . import views

app_name='core'
urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('index/<str:summary_file_path>/', views.index, name='index_with_path'),
    path('download/<str:file_full_path>/', views.download_file, name='download_file'),
    path('reconcile/<str:file_1>/<str:file_2>', views.reconcile, name='reconcile'),
    path('download_sample_file/', views.download_sample_file, name='download_sample_file'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path("logout", views.logout_view, name= "logout"),
]
