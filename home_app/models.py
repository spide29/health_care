from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    LICENSE_TYPES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    license_number = models.CharField(max_length=20, blank=True, null=True)
    user_type = models.CharField(max_length=10, choices=LICENSE_TYPES)
    @property
    def is_doctor(self):
        return self.user_type == 'doctor'
    @property
    def is_patient(self):
        return self.user_type == 'patient'
    def save(self, *args, **kwargs):
        if self.user_type == 'patient':
            self.license_number = None
        super().save(*args, **kwargs)

# class DoctorInfo(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_info')
#     dob = models.DateField()
#     specialization = models.CharField(max_length=100)
#     degree = models.CharField(max_length=100)
#     experience = models.PositiveIntegerField()

#     def __str__(self):
#         return self.user.username