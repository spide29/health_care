from django.db import models
from home_app.models import CustomUser
from datetime import datetime, timedelta
from django.db import models
from django.utils import timezone


# Create your models here.
class DoctorInfo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_info')
    dob = models.DateField()
    specialization = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    description = models.TextField()
    address = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username
        
class Leave(models.Model):
    doctor_info = models.ForeignKey(DoctorInfo, on_delete=models.CASCADE, related_name='leaves')
    starting_date = models.DateField()
    ending_date = models.DateField()
    phone_no = models.CharField(max_length=20)

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
            while current_datetime <= end_datetime:
                slots.append(current_datetime.time().strftime('%H:%M:%S'))
                current_datetime += timedelta(minutes=self.time_slot_duration)
            time_slots[current_date.strftime('%Y-%m-%d')] = slots
            current_date += timedelta(days=1)

        return time_slots
