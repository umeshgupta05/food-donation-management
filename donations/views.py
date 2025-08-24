
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Donation, Claim
from accounts.models import DonorProfile, ReceiverProfile
from django import forms
from django.utils import timezone

class DonationForm(forms.ModelForm):
	class Meta:
		model = Donation
		fields = ['food_type', 'description', 'quantity', 'pickup_location', 'expiry_time']

@login_required
def create_donation(request):
	if request.user.role != 'donor':
		messages.error(request, 'Only donors can post donations.')
		return redirect('dashboard')
	if request.method == 'POST':
		form = DonationForm(request.POST)
		if form.is_valid():
			donor_profile = DonorProfile.objects.get(user=request.user)
			donation = form.save(commit=False)
			donation.donor = donor_profile
			donation.save()
			messages.success(request, 'Donation posted successfully!')
			return redirect('donation_history')
	else:
		form = DonationForm()
	return render(request, 'donations/create_donation.html', {'form': form})

@login_required
def available_donations(request):
	donations = Donation.objects.filter(status='available', expiry_time__gt=timezone.now())
	return render(request, 'donations/available_donations.html', {'donations': donations})

@login_required
def claim_donation(request, donation_id):
	if request.user.role != 'receiver':
		messages.error(request, 'Only receivers can claim donations.')
		return redirect('dashboard')
	donation = get_object_or_404(Donation, id=donation_id, status='available')
	receiver_profile = ReceiverProfile.objects.get(user=request.user)
	Claim.objects.create(donation=donation, receiver=receiver_profile, status='pending')
	donation.status = 'claimed'
	donation.save()
	messages.success(request, 'Donation claimed! Await approval.')
	return redirect('donation_history')

@login_required
def donation_history(request):
	if request.user.role == 'donor':
		donor_profile = DonorProfile.objects.get(user=request.user)
		donations = Donation.objects.filter(donor=donor_profile)
		return render(request, 'donations/donation_history.html', {'donations': donations})
	elif request.user.role == 'receiver':
		receiver_profile = ReceiverProfile.objects.get(user=request.user)
		claims = Claim.objects.filter(receiver=receiver_profile)
		return render(request, 'donations/claim_history.html', {'claims': claims})
	else:
		return redirect('dashboard')
