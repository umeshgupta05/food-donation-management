from django.urls import path
from . import views
from .views_auth import user_logout

urlpatterns = [
    path('', views.home, name='home'),
    path('register/donor/', views.donor_register, name='donor_register'),
    path('register/receiver/', views.receiver_register, name='receiver_register'),
    path('login/', views.user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
