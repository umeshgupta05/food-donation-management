
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	ROLE_CHOICES = [
		('donor', 'Donor'),
		('receiver', 'Receiver'),
		('admin', 'Admin'),
	]
	role = models.CharField(max_length=10, choices=ROLE_CHOICES)
	phone_number = models.CharField(max_length=15, blank=True)

class DonorProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	organization_name = models.CharField(max_length=100, blank=True, null=True)
	address = models.TextField()

	def __str__(self):
		return self.user.username

class ReceiverProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	org_name = models.CharField(max_length=100)
	registration_number = models.CharField(max_length=50)
	address = models.TextField()
	is_verified = models.BooleanField(default=False)

	def __str__(self):
		return self.org_name
