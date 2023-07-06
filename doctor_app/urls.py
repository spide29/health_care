from django.urls import path
from .views import DoctorInfoView, DoctorInfoDetailView

urlpatterns = [
    path('doctor-info/post-update/', DoctorInfoView.as_view(), name='doctor-info'),
    path('doctor-info/get/', DoctorInfoDetailView.as_view(), name='doctor-info-detail'),

]
