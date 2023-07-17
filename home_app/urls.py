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
from . import views
from .views import DoctorSignupView, PatientSignupView, login_view,logout_api, DoctorListAPIView, PatientListAPIView
from .views import UserDetailView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('',views.home,name='home'),
    path('doctor-signup/',views.doctor_signup,name='doctor_signup'),
    path('patient-signup/',views.patient_signup,name='patient_signup'),
    path('login/',views.signin,name='login'),
    # path('doctor_portal/', views.doctor_portal, name='doctor_portal'),
    # path('patient_portal/', views.patient_portal, name='patient_portal'),



########################### API

    path('all-users-get/', UserDetailView.as_view(), name='user-detail'),
    path('signup/doctor/', DoctorSignupView.as_view(), name='doctor_signup'),
    path('signup/patient/', PatientSignupView.as_view(), name='patient_signup'),
    path('login-user/', login_view, name='login'),
    path('logout-user/', logout_api, name='logout'),
    path('get-doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    path('get-patients/', PatientListAPIView.as_view(), name='patient-list'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
