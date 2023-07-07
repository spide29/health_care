from django.http import HttpResponse
from rest_framework import generics
from .serializers import DoctorSignupSerializer, PatientSignupSerializer,DoctorSerializer, PatientSerializer,CustomUserSerializer
from .models import CustomUser
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


class UserDetailView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

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