def home(request):
	return render(request, 'home.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User, DonorProfile, ReceiverProfile
from django import forms

class DonorRegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	address = forms.CharField(widget=forms.Textarea, required=True)
	organization_name = forms.CharField(required=False)
	class Meta:
		model = User
		fields = ['username', 'email', 'phone_number', 'password']

class ReceiverRegisterForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	org_name = forms.CharField(max_length=100)
	registration_number = forms.CharField(max_length=50)
	address = forms.CharField(widget=forms.Textarea)
	class Meta:
		model = User
		fields = ['username', 'email', 'phone_number', 'password']

def donor_register(request):
	if request.method == 'POST':
		form = DonorRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.role = 'donor'
			user.save()
			
			# Get data from the form's cleaned_data
			address = form.cleaned_data.get('address', '')
			organization_name = form.cleaned_data.get('organization_name', '')
			
			# Create the donor profile and print debug info
			print(f"Creating DonorProfile for user {user.id} with address: {address}")
			DonorProfile.objects.create(
				user=user, 
				address=address,
				organization_name=organization_name
			)
			messages.success(request, 'Donor registered successfully!')
			return redirect('login')
	else:
		form = DonorRegisterForm()
	return render(request, 'accounts/donor_register.html', {'form': form})

def receiver_register(request):
	if request.method == 'POST':
		form = ReceiverRegisterForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.set_password(form.cleaned_data['password'])
			user.role = 'receiver'
			user.save()
			ReceiverProfile.objects.create(
				user=user,
				org_name=form.cleaned_data['org_name'],
				registration_number=form.cleaned_data['registration_number'],
				address=form.cleaned_data['address'],
			)
			messages.success(request, 'Receiver registered successfully! Await admin approval.')
			return redirect('login')
	else:
		form = ReceiverRegisterForm()
	return render(request, 'accounts/receiver_register.html', {'form': form})


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput)

def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			
			# Debug authentication process
			print(f"Attempting to authenticate user: {username}")
			user = authenticate(request, username=username, password=password)
			
			if user is not None:
				print(f"Authentication successful for: {username}")
				login(request, user)
				messages.success(request, f"Welcome back, {username}!")
				return redirect('dashboard')
			else:
				print(f"Authentication failed for: {username}")
				messages.error(request, 'Invalid credentials. Please check your username and password.')
	else:
		form = LoginForm()
	return render(request, 'accounts/login.html', {'form': form})

from django.contrib.auth.decorators import login_required
from donations.models import Donation, Claim
from django.utils import timezone

@login_required
def dashboard(request):
	context = {}
	
	if request.user.role == 'donor':
		try:
			donor_profile = DonorProfile.objects.get(user=request.user)
			# Get counts for different donation statuses
			active_donations = Donation.objects.filter(donor=donor_profile, status='available').count()
			claimed_donations = Donation.objects.filter(donor=donor_profile, status='claimed').count()
			completed_donations = Donation.objects.filter(donor=donor_profile, status='completed').count()
			
			# Get recent donations
			recent_donations = Donation.objects.filter(donor=donor_profile).order_by('-created_at')[:5]
			
			context = {
				'active_donations': active_donations,
				'claimed_donations': claimed_donations,
				'completed_donations': completed_donations,
				'recent_donations': recent_donations
			}
		except DonorProfile.DoesNotExist:
			pass
	
	elif request.user.role == 'receiver':
		try:
			receiver_profile = ReceiverProfile.objects.get(user=request.user)
			# Get counts for available donations and claims
			available_donations = Donation.objects.filter(status='available', expiry_time__gt=timezone.now()).count()
			pending_claims = Claim.objects.filter(receiver=receiver_profile, status='pending').count()
			completed_claims = Claim.objects.filter(receiver=receiver_profile, status='approved').count()
			
			# Get recent claims
			recent_claims = Claim.objects.filter(receiver=receiver_profile).order_by('-claimed_at')[:5]
			
			context = {
				'available_donations': available_donations,
				'pending_claims': pending_claims,
				'completed_claims': completed_claims,
				'recent_claims': recent_claims
			}
		except ReceiverProfile.DoesNotExist:
			pass
	
	elif request.user.role == 'admin' or request.user.is_staff:
		# Admin dashboard statistics
		total_users = User.objects.count()
		pending_ngos = ReceiverProfile.objects.filter(is_verified=False).count()
		total_donations = Donation.objects.count()
		total_claims = Claim.objects.count()
		
		# Get recent donations and claims for activity feed
		recent_donations = Donation.objects.all().order_by('-created_at')[:5]
		recent_claims = Claim.objects.all().order_by('-claimed_at')[:5]
		
		context = {
			'total_users': total_users,
			'pending_ngos': pending_ngos,
			'total_donations': total_donations,
			'total_claims': total_claims,
			'recent_donations': recent_donations,
			'recent_claims': recent_claims
		}
	
	return render(request, 'accounts/dashboard.html', context)
