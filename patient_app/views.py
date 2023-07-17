from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

# Create your views here.
from rest_framework import generics
from .models import PatientInfo
from .serializers import PatientInfoSerializer, PatientInfoGetSerializer, AppointmentBookingSerializer


def patient_portal(request):
    return render(request, 'home_page/patient_portal.html')

# class PatientInfoCreateView(generics.CreateAPIView):
#     permission_classes = [IsAuthenticated]

#     queryset = PatientInfo.objects.all()
#     serializer_class = PatientInfoSerializer

class PatientInfoCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PatientInfo.objects.all()
    serializer_class = PatientInfoSerializer

    def perform_create(self, serializer):
        user = self.request.user
        patient_info = PatientInfo.objects.filter(user=user).first()

        if patient_info:
            serializer.update(patient_info, serializer.validated_data)
        else:
            serializer.save(user=user)

class PatientInfoDetailView(ListAPIView):
    queryset = PatientInfo.objects.all()
    serializer_class = PatientInfoGetSerializer


from rest_framework import generics
from rest_framework.response import Response
from datetime import datetime

class AppointmentBookingView(generics.CreateAPIView):
    serializer_class = AppointmentBookingSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor_id = serializer.validated_data['doctor']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']
        
        # Perform the appointment booking logic here
        # You can access the doctor ID, date, and time to create a booking instance
        
        # Example logic:
        # booking = Booking(doctor_info_id=doctor_id, start_date=date, end_date=date, starting_time=time, ending_time=time)
        # booking.save()

        return Response({'message': 'Appointment booked successfully'})
