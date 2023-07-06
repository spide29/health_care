from rest_framework import serializers
from .models import CustomUser
from doctor_app.models import DoctorInfo
from doctor_app.serializers import DoctorInfoSerializer

# class UserSignupSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True)

#     class Meta:
#         model = CustomUser
#         fields = ['license_number', 'first_name', 'last_name', 'username', 'email', 'password', 'password2']
#         extra_kwargs = {
#             'password': {'write_only': True},
#         }

#     def validate(self, data):
#         password = data.get('password')
#         password2 = data.pop('password2')
#         if password != password2:
#             raise serializers.ValidationError("Passwords do not match.")
#         return data

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = CustomUser(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user
from rest_framework_simplejwt.tokens import RefreshToken

class DoctorSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['license_number', 'first_name', 'last_name', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(user_type='doctor', **validated_data)
        user.set_password(password)
        user.save()
        return user

class PatientSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        password2 = data.pop('password2')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(user_type='patient', **validated_data)
        user.set_password(password)
        user.save()
        return user

class DoctorSerializer(serializers.ModelSerializer):
    doctor_info = DoctorInfoSerializer(read_only=True)  # Nested serializer for DoctorInfo

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'doctor_info')

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name','last_name', 'license_number')  # Add more fields as per your requirements