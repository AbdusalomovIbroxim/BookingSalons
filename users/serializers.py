from rest_framework import serializers
from .models import User

class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        help_text="Номер телефона в международном формате"
    )

    class Meta:
        swagger_schema_fields = {
            "example": {
                "phone_number": "+79001234567"
            }
        }

class VerifyOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        help_text="Номер телефона в международном формате"
    )
    otp = serializers.CharField(
        help_text="Код подтверждения"
    )

    class Meta:
        swagger_schema_fields = {
            "example": {
                "phone_number": "+79001234567",
                "otp": "11111"
            }
        }

class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        required=False,
        help_text="Имя пользователя"
    )
    last_name = serializers.CharField(
        required=False,
        help_text="Фамилия пользователя"
    )

    class Meta:
        swagger_schema_fields = {
            "example": {
                "first_name": "Иван",
                "last_name": "Иванов"
            }
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number', 'first_name', 'last_name']
        read_only_fields = ['phone_number']
        swagger_schema_fields = {
            "example": {
                "phone_number": "+79001234567",
                "first_name": "Иван",
                "last_name": "Иванов"
            }
        } 