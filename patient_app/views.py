from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView

# Create your views here.
from rest_framework import generics
from .models import PatientInfo
from .serializers import PatientInfoSerializer, PatientInfoGetSerializer

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
