from django.db import models
from home_app.models import CustomUser

# Create your models here.
class DoctorInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_info')
    dob = models.DateField()
    specialization = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username