# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from .models import CustomUser
# from django.contrib.auth import logout


# def home(request):
#     return render(request,'home.html')

# def doctor_signup(request):
#     if request.method == "POST":
#         lic = request.POST['lic']
#         username = request.POST['username']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']

#         myuser = CustomUser.objects.create_user(username=username, email=email, password=pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         myuser.user_type = 'doctor'
#         myuser.license_number = lic
#         myuser.save()

#         return redirect('signin')
    
#     return render(request, "doctor_signup.html")

# def signup(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
#         license_number = request.POST.get('lic', None)

#         myuser = CustomUser.objects.create_user(username=username, email=email, password=pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         myuser.user_type = 'patient'

#         if license_number:
#             myuser.license_number = license_number
#         else:
#             myuser.license_number = None
#         myuser.save()
#         return redirect('signin')
#     return render(request, 'signup.html')

# def signin(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
#         user = authenticate(request, username=username, password=pass1)

#         if user is not None:
#             login(request, user)
#             if user.is_doctor:
#                 return redirect('doctor_portal')
#             elif user.is_patient:
#                 return redirect('patient_portal')
#         else:
#             return redirect('signin')
#     return render(request, 'home.html')

# def signout(request):
#     logout(request)
#     if request.user.is_authenticated:
#         request.user.is_active = False
#         request.user.save()
#     return redirect('home')

# def doctor_portal(request):
#     return render(request, 'doctor_portal.html')

# def patient_portal(request):
#     return render(request, 'patient_portal.html')

from django.http import HttpResponse
from rest_framework import generics
from .serializers import DoctorSignupSerializer, PatientSignupSerializer,DoctorSerializer, PatientSerializer
from .models import CustomUser
from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
    ),
    responses={
        200: 'Successful login',
        401: 'Invalid credentials',
    }
)
@api_view(['POST'])
@csrf_exempt
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        user.last_login = timezone.now()
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        if user.is_doctor:
            message = "Welcome to the doctor portal!"
        elif user.is_patient:
            message = "Welcome to the patient portal!"
        else:
            message = "Welcome!"

        return Response({'message': message, 'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=401)

from django.contrib.auth import logout 
# @api_view(['POST'])
# def logout_api(request):
#     logout(request)
#     return Response({'message': 'Logged out successfully'})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_api(request):
    request.user.auth_token.delete()
    return HttpResponse("user logout")
    # return redirect("/login_user")

class DoctorSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = DoctorSignupSerializer

class PatientSignupView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = PatientSignupSerializer


class DoctorListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(user_type='doctor')
    serializer_class = DoctorSerializer

class PatientListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(user_type='patient')
    serializer_class = PatientSerializer