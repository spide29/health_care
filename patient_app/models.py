from django.db import models
from home_app.models import CustomUser

# Create your models here.
class PatientInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_info')
    dob = models.DateField()
    disease = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
