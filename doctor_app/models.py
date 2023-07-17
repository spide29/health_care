from django.db import models
from home_app.models import CustomUser
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone


# Create your models here.
class DoctorInfo(models.Model):
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

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_info')
    dob = models.DateField()
    specialization = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)
    state = models.CharField(max_length=100, choices=STATE_CHOICES)

    def __str__(self):
        return self.user.username
        
class Leave(models.Model):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, related_name='leaves')
    starting_date = models.DateField()
    ending_date = models.DateField()
    # phone_no = models.CharField(max_length=20)

    def __str__(self):
        return f"Leave ID: {self.id} - Doctor: {self.doctor_info.user.username}"

    def save(self, *args, **kwargs):
        if not self.pk and self.doctor_info_id is None:
            self.doctor_info_id = self.doctor_info.user_id
        super().save(*args, **kwargs)



class Booking(models.Model):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    starting_time = models.TimeField()
    ending_time = models.TimeField()
    time_slot_duration = models.PositiveIntegerField(default=30)  # Duration in minutes for each time slot

    def __str__(self):
        return f"Booking ID: {self.id} - Doctor: {self.doctor_info.user.username} - Start Date: {self.start_date} - End Date: {self.end_date}"

    def generate_time_slots(self):
        time_slots = {}

        current_date = self.start_date
        while current_date <= self.end_date:
            slots = []
            current_datetime = datetime.combine(current_date, self.starting_time)
            end_datetime = datetime.combine(current_date, self.ending_time)
            while current_datetime < end_datetime:  # Use '<' instead of '<=' to exclude ending_time
                slots.append(current_datetime.time().strftime('%I:%M %p'))
                current_datetime += timedelta(minutes=self.time_slot_duration)
            time_slots[current_date.strftime('%Y-%m-%d')] = slots
            current_date += timedelta(days=1)

        return time_slots