from django.urls import path
from .views import PatientInfoCreateView,PatientInfoDetailView, AppointmentBookingView
from . import views

urlpatterns = [


    path('patient_portal/', views.patient_portal, name='patient_portal'),


    path('patient-info/post/', PatientInfoCreateView.as_view(), name='patient-info-create'),
    path('patient-info/get/', PatientInfoDetailView.as_view(), name='doctor-info-detail'),
    path('book-appointment/', AppointmentBookingView.as_view(), name='book-appointment'),
    # Add other URLs as needed
]
