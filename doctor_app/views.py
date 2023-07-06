from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from .serializers import DoctorInfoSerializer,DoctorInfoGetSerializer
from .models import DoctorInfo

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
