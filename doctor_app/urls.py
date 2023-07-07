from django.urls import path
from .views import DoctorInfoView, DoctorInfoDetailView, LeaveListCreateAPIView,BookingCreateUpdateView,BookingRetrieveView

urlpatterns = [
    path('doctor-info/post-update/', DoctorInfoView.as_view(), name='doctor-info'),
    path('doctor-info/get/', DoctorInfoDetailView.as_view(), name='doctor-info-detail'),
    path('doctor-info/leave/', LeaveListCreateAPIView.as_view(), name='create_or_update_leave'),
    path('doctor-info/bookings/', BookingCreateUpdateView.as_view(), name='booking-create-update'),
    path('doctor-info/bookings/<int:pk>/', BookingRetrieveView.as_view(), name='booking-retrieve'),
]
