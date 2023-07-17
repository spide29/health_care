from django.shortcuts import render
from rest_framework import generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from .serializers import DoctorInfoSerializer,DoctorInfoGetSerializer, LeaveSerializer, BookingSerializer, BookingUpdateSerializer
from .models import DoctorInfo, Leave, Booking
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from rest_framework.generics import UpdateAPIView,DestroyAPIView



def doctor_portal(request):
    return render(request, 'home_page/doctor_portal.html')

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

######################################################### Leave

class DoctorInfoDetailView(ListAPIView):
    queryset = DoctorInfo.objects.all()
    serializer_class = DoctorInfoGetSerializer

class LeaveListCreateAPIView(generics.ListCreateAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer

    def perform_create(self, serializer):
        serializer.save(doctor_info=self.request.user.doctor_info)

class LeaveDeleteAPIView(DestroyAPIView):
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    lookup_field = 'id'

######################################################### Bokking
from rest_framework import serializers
from django.utils import timezone

class BookingCreateUpdateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        doctor_info = self.request.user.doctor_info  # Retrieve the doctor_info from the requesting user
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        leave_exists = Leave.objects.filter(doctor_info=doctor_info, starting_date__lte=end_date, ending_date__gte=start_date).exists()
        if leave_exists:
            raise serializers.ValidationError("You are on leave for the specified date range")
        slot_exists = Booking.objects.filter(doctor_info=doctor_info, start_date__lte=end_date, end_date__gte=start_date).exists()
        if slot_exists:
            raise serializers.ValidationError("Slot already exists within the specified date range")
        serializer.save(doctor_info=doctor_info)



class BookingUpdateView(UpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingUpdateSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data.get('start_date', instance.start_date)
        end_date = serializer.validated_data.get('end_date', instance.end_date)
        bookings = Booking.objects.filter(
            doctor_info=instance.doctor_info,
            start_date__lte=end_date,
            end_date__gte=start_date
        ).exclude(pk=instance.pk)

        if bookings.exists():
            return Response({'error': 'The time slot is already present.'}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)


class BookingRetrieveView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class BookingDeleteView(DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    lookup_field = 'id'
#########################################################


# class DoctorSearchAPIView(generics.ListAPIView):
#     serializer_class = DoctorInfoGetSerializer
#     def get_queryset(self):
#         specialization = self.kwargs.get('specialization', '')
#         state = self.request.query_params.get('state', '')
#         queryset = DoctorInfo.objects.all()
#         if specialization:
#             queryset = queryset.filter(specialization__icontains=specialization)
#         if state:
#             queryset = queryset.filter(state__icontains=state)
#         if specialization and not queryset.exists():
#             raise NotFound(detail="No doctors available with the specified criteria.")
#         return queryset
# class DoctorSearchAPIView(generics.ListAPIView):
#     serializer_class = DoctorInfoGetSerializer

#     def get_queryset(self):
#         specialization = self.kwargs.get('specialization', '')
#         state = self.kwargs.get('state', '')
#         queryset = DoctorInfo.objects.all()
#         if specialization:
#             queryset = queryset.filter(specialization__icontains=specialization)
#         if state:
#             queryset = queryset.filter(state__icontains=state)
#         if not specialization and not state:
#             raise NotFound(detail="Please provide a specialization or state for the search.")
#         return queryset
    
class DoctorSearchView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            # openapi.Parameter('experience', openapi.IN_QUERY, description='Search by experience', type=openapi.TYPE_INTEGER),
            openapi.Parameter('specialization', openapi.IN_QUERY, description='Search by specialization', type=openapi.TYPE_STRING),
            openapi.Parameter('state', openapi.IN_QUERY, description='Search by state', type=openapi.TYPE_STRING),
        ],
        responses={200: DoctorInfoGetSerializer(many=True)}
    )
    def get(self, request):
        # experience = request.query_params.get('experience')
        specialization = request.query_params.get('specialization')
        state = request.query_params.get('state')
        doctors = DoctorInfo.objects.all()

        # if experience:
        #     doctors = doctors.filter(experience__gte=experience)
        if specialization:
            doctors = doctors.filter(specialization__icontains=specialization)
        if state:
            doctors = doctors.filter(state=state)
        serializer = DoctorInfoGetSerializer(doctors, many=True)
        return Response(serializer.data)


