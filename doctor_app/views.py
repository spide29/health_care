from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from .serializers import DoctorInfoSerializer,DoctorInfoGetSerializer, LeaveSerializer
from .models import DoctorInfo, Leave
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response



class DoctorInfoView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = DoctorInfo.objects.all()
    serializer_class = DoctorInfoSerializer

    def perform_create(self, serializer):
        user = self.request.user
        doctor_info = DoctorInfo.objects.filter(user=user).first()

        if doctor_info:
            serializer.update(doctor_info, serializer.validated_data)
        else:
            serializer.save(user=user)

# class DoctorInfoDetailView(RetrieveAPIView):
#     queryset = DoctorInfo.objects.all()
#     serializer_class = DoctorInfoGetSerializer

class DoctorInfoDetailView(ListAPIView):
    queryset = DoctorInfo.objects.all()
    serializer_class = DoctorInfoGetSerializer


class LeaveListCreateAPIView(generics.ListCreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

    def perform_create(self, serializer):
        serializer.save(doctor_info=self.request.user.doctor_info)

from rest_framework import generics

from .models import Booking
from .serializers import BookingSerializer

class BookingCreateUpdateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        doctor_info = self.request.user.doctor_info
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        leave_exists = Leave.objects.filter(doctor_info=doctor_info, starting_date__lte=end_date, ending_date__gte=start_date).exists()

        if leave_exists:
            raise serializers.ValidationError("You are on leave for the specified date range")
        slot_exists = Booking.objects.filter(doctor_info=doctor_info, start_date__lte=end_date, end_date__gte=start_date).exists()

        if slot_exists:
            raise serializers.ValidationError("Slot already exists within the specified date range")

        serializer.save(doctor_info=doctor_info)

class BookingRetrieveView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
