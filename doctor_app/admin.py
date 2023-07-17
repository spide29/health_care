from django.contrib import admin
from .models import DoctorInfo, Booking, Leave

# Register your models here.
admin.site.register(DoctorInfo)
admin.site.register(Booking)
admin.site.register(Leave)

