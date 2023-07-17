from . import views

from django.urls import path
from .views import DoctorInfoView, DoctorInfoDetailView, LeaveListCreateAPIView,BookingCreateUpdateView,BookingRetrieveView
from .views import  DoctorSearchView, BookingUpdateView, BookingDeleteView, LeaveDeleteAPIView
urlpatterns = [


    path('doctor_portal/', views.doctor_portal, name='doctor_portal'),

    
    path('doctor-info/post-update/', DoctorInfoView.as_view(), name='doctor-info'),
    path('doctor-info/get/', DoctorInfoDetailView.as_view(), name='doctor-info-detail'),
    path('doctor-info/leave/', LeaveListCreateAPIView.as_view(), name='create_or_update_leave'),
    path('doctor-info/leaves/<int:id>/', LeaveDeleteAPIView.as_view(), name='leave-delete'),
    path('doctor-info/bookings/', BookingCreateUpdateView.as_view(), name='booking-create-update'),
    path('doctor-info/bookings/<int:pk>/', BookingRetrieveView.as_view(), name='booking-retrieve'),
    # path('doctor-info/search/<str:specialization>/<str:state>/', DoctorSearchAPIView.as_view(), name='doctor-search'),
    # path('doctor-info/search-specialization/<str:specialization>/', DoctorSearchAPIView.as_view(), name='doctor-search'),
    # path('doctor-info/search-state/<str:state>/', DoctorSearchAPIView.as_view(), name='doctor-search'),
    path('doctor-info/bookings-update/<int:pk>/', BookingUpdateView.as_view(), name='booking-update'),
    path('doctor-info/bookings/<int:id>/', BookingDeleteView.as_view(), name='booking-delete'),
    path('doctor-info/filter', DoctorSearchView.as_view(), name='doctor-info-list'),

]

