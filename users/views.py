from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
from .models import User
from .serializers import (
    SendOTPSerializer,
    VerifyOTPSerializer,
    UpdateProfileSerializer,
    UserProfileSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import random

# Create your views here.

class SendOTPView(APIView):
    """
    API endpoint для отправки OTP на номер телефона.
    
    Пример запроса:
    ```json
    {
        "phone_number": "+79001234567"
    }
    ```
    """
    permission_classes = [AllowAny]
    serializer_class = SendOTPSerializer

    @swagger_auto_schema(
        request_body=SendOTPSerializer,
        responses={
            200: openapi.Response(
                description="OTP успешно отправлен",
                examples={
                    "application/json": {
                        "message": "OTP sent successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Ошибка валидации",
                examples={
                    "application/json": {
                        "error": "Phone number is required"
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        
        # Generate OTP (for development, always use 11111)
        otp = '11111'
        
        user, created = User.objects.get_or_create(
            phone_number=phone_number,
            defaults={'username': phone_number}
        )
        
        user.otp_code = otp
        user.otp_created_at = timezone.now()
        user.save()

        return Response({'message': 'OTP sent successfully'})

class VerifyOTPView(APIView):
    """
    API endpoint для проверки OTP и получения JWT токенов.
    
    Пример запроса:
    ```json
    {
        "phone_number": "+79001234567",
        "otp": "11111"
    }
    ```
    """
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    @swagger_auto_schema(
        request_body=VerifyOTPSerializer,
        responses={
            200: openapi.Response(
                description="OTP успешно проверен",
                examples={
                    "application/json": {
                        "message": "OTP verified successfully"
                    }
                }
            ),
            400: openapi.Response(
                description="Ошибка валидации",
                examples={
                    "application/json": {
                        "error": "Invalid OTP"
                    }
                }
            ),
            404: openapi.Response(
                description="Пользователь не найден",
                examples={
                    "application/json": {
                        "error": "User not found"
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        phone_number = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, 
                          status=status.HTTP_404_NOT_FOUND)

        # Check if OTP is expired (5 minutes)
        if user.otp_created_at and timezone.now() - user.otp_created_at > timedelta(minutes=5):
            return Response({'error': 'OTP has expired'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        if user.otp_code != otp:
            return Response({'error': 'Invalid OTP'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Clear OTP after successful verification
        user.otp_code = None
        user.otp_created_at = None
        user.save()

        return Response({'message': 'OTP verified successfully'})

class UpdateProfileView(APIView):
    """
    API endpoint для обновления профиля пользователя.
    
    Пример запроса:
    ```json
    {
        "first_name": "Иван",
        "last_name": "Иванов"
    }
    ```
    """
    serializer_class = UpdateProfileSerializer

    @swagger_auto_schema(
        request_body=UpdateProfileSerializer,
        responses={
            200: openapi.Response(
                description="Профиль успешно обновлен",
                examples={
                    "application/json": {
                        "message": "Profile updated successfully",
                        "user": {
                            "phone_number": "+79001234567",
                            "first_name": "Иван",
                            "last_name": "Иванов"
                        }
                    }
                }
            ),
            400: openapi.Response(
                description="Ошибка валидации",
                examples={
                    "application/json": {
                        "error": "Invalid data"
                    }
                }
            )
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        if 'first_name' in serializer.validated_data:
            user.first_name = serializer.validated_data['first_name']
        if 'last_name' in serializer.validated_data:
            user.last_name = serializer.validated_data['last_name']

        user.save()

        return Response({
            'message': 'Profile updated successfully',
            'user': UserProfileSerializer(user).data
        })
