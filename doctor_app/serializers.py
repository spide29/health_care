from rest_framework import serializers
from .models import DoctorInfo

class DoctorInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorInfo
        fields = ['id', 'dob', 'specialization', 'degree', 'experience']
        # read_only=[' user']

class DoctorInfoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorInfo
        fields = '__all__'
