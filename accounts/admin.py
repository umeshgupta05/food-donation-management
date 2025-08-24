
from django.contrib import admin
from .models import User, DonorProfile, ReceiverProfile

admin.site.register(User)
admin.site.register(DonorProfile)
admin.site.register(ReceiverProfile)
