"""health_care URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from . import views
from .views import DoctorSignupView, PatientSignupView, login_view,logout_api, DoctorListAPIView, PatientListAPIView
from .views import UserDetailView

urlpatterns = [
    path('api/users-get/', UserDetailView.as_view(), name='user-detail'),
    path('api/signup/doctor/', DoctorSignupView.as_view(), name='doctor_signup'),
    path('api/signup/patient/', PatientSignupView.as_view(), name='patient_signup'),
    path('api/login/', login_view, name='login'),
    path('api/logout/', logout_api, name='logout'),
    path('api/get-doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('api/get-patients/', PatientListAPIView.as_view(), name='patient-list'),
]
