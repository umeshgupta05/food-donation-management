
from django.db import models
from accounts.models import DonorProfile, ReceiverProfile

class Donation(models.Model):
	FOOD_TYPE_CHOICES = [
		('veg', 'Veg'),
		('non-veg', 'Non-Veg'),
	]
	STATUS_CHOICES = [
		('available', 'Available'),
		('claimed', 'Claimed'),
		('collected', 'Collected'),
		('completed', 'Completed'),
	]
	donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE)
	food_type = models.CharField(max_length=10, choices=FOOD_TYPE_CHOICES)
	description = models.TextField()
	quantity = models.CharField(max_length=50)
	pickup_location = models.TextField()
	expiry_time = models.DateTimeField()
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.food_type} - {self.quantity} by {self.donor}"

class Claim(models.Model):
	STATUS_CHOICES = [
		('pending', 'Pending'),
		('approved', 'Approved'),
		('rejected', 'Rejected'),
	]
	donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
	receiver = models.ForeignKey(ReceiverProfile, on_delete=models.CASCADE)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
	claimed_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.receiver} claims {self.donation}"
