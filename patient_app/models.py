from django.db import models
from home_app.models import CustomUser

# Create your models here.
class PatientInfo(models.Model):
    STATE_CHOICES = (
        ('Andhra Pradesh', 'Andhra Pradesh (Amaravati)'),
        ('Arunachal Pradesh', 'Arunachal Pradesh (Itanagar)'),
        ('Assam', 'Assam (Dispur)'),
        ('Bihar', 'Bihar (Patna)'),
        ('Chhattisgarh', 'Chhattisgarh (Raipur)'),
        ('Goa', 'Goa (Panaji)'),
        ('Gujarat', 'Gujarat (Gandhinagar)'),
        ('Haryana', 'Haryana (Chandigarh)'),
        ('Himachal Pradesh', 'Himachal Pradesh (Shimla)'),
        ('Jharkhand', 'Jharkhand (Ranchi)'),
        ('Karnataka', 'Karnataka (Bangalore)'),
        ('Kerala', 'Kerala (Thiruvananthapuram)'),
        ('Madhya Pradesh', 'Madhya Pradesh (Bhopal)'),
        ('Maharashtra', 'Maharashtra (Mumbai)'),
        ('Manipur', 'Manipur (Imphal)'),
        ('Meghalaya', 'Meghalaya (Shillong)'),
        ('Mizoram', 'Mizoram (Aizawl)'),
        ('Nagaland', 'Nagaland (Kohima)'),
        ('Odisha', 'Odisha (Bhubaneshwar)'),
        ('Punjab', 'Punjab (Chandigarh)'),
        ('Rajasthan', 'Rajasthan (Jaipur)'),
        ('Sikkim', 'Sikkim (Gangtok)'),
        ('Tamil Nadu', 'Tamil Nadu (Chennai)'),
        ('Telangana', 'Telangana (Hyderabad)'),
        ('Tripura', 'Tripura (Agartala)'),
        ('Uttarakhand', 'Uttarakhand (Dehradun)'),
        ('Uttar Pradesh', 'Uttar Pradesh (Lucknow)'),
        ('West Bengal', 'West Bengal (Kolkata)'),
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands (Port Blair)'),
        ('Chandigarh', 'Chandigarh (Chandigarh)'),
        ('Dadra and Nagar Haveli and Daman & Diu', 'Dadra and Nagar Haveli and Daman & Diu (Daman)'),
        ('The Government of NCT of Delhi', 'The Government of NCT of Delhi (Delhi)'),
        ('Jammu & Kashmir', 'Jammu & Kashmir (Srinagar-S*, Jammu-W*)'),
        ('Ladakh', 'Ladakh (Leh)'),
        ('Lakshadweep', 'Lakshadweep (Kavaratti)'),
        ('Puducherry', 'Puducherry (Puducherry)'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_info')
    dob = models.DateField()
    disease = models.CharField(max_length=100)
    description = models.TextField()
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    state = models.CharField(max_length=100, choices=STATE_CHOICES)

    def __str__(self):
        return self.user.username