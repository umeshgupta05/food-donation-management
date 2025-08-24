from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_donation, name='create_donation'),
    path('available/', views.available_donations, name='available_donations'),
    path('claim/<int:donation_id>/', views.claim_donation, name='claim_donation'),
    path('history/', views.donation_history, name='donation_history'),
]
