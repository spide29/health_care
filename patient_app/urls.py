from django.urls import path
from .views import PatientInfoCreateView,PatientInfoDetailView

urlpatterns = [
    path('patient-info/post/', PatientInfoCreateView.as_view(), name='patient-info-create'),
    path('patient-info/get/', PatientInfoDetailView.as_view(), name='doctor-info-detail'),
    # Add other URLs as needed
]
