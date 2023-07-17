from rest_framework import serializers
from .models import PatientInfo

class PatientInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInfo
        fields = ['dob', 'disease', 'description', 'address','state' , 'phone_no']

class PatientInfoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInfo
        fields = '__all__'


class AppointmentBookingSerializer(serializers.Serializer):
    doctor = serializers.IntegerField()
    date = serializers.DateField()
    time = serializers.TimeField()