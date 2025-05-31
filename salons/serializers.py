from rest_framework import serializers
from .models import Salon, Staff, Booking, SalonPhoto
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'first_name', 'last_name']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'salon', 'full_name', 'services']
        swagger_schema_fields = {
            "example": {
                "salon": 1,
                "full_name": "Анна Петрова",
                "services": ["Стрижка", "Окрашивание", "Укладка"]
            }
        }

class SalonPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalonPhoto
        fields = ['id', 'image', 'order', 'is_main']

class SalonSerializer(serializers.ModelSerializer):
    photos = SalonPhotoSerializer(many=True, read_only=True)
    staff = StaffSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Salon
        fields = ['id', 'title', 'description', 'location_lat', 
                 'location_lon', 'yandex_link', 'owner', 'staff', 'photos']
        read_only_fields = ['owner']
        swagger_schema_fields = {
            "example": {
                "title": "Салон красоты 'Элегант'",
                "description": "Салон красоты с полным спектром услуг",
                "location_lat": 55.7558,
                "location_lon": 37.6173,
                "yandex_link": "https://yandex.ru/maps/..."
            }
        }

class BookingSerializer(serializers.ModelSerializer):
    salon = SalonSerializer(read_only=True)
    staff = StaffSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'salon', 'staff', 'client', 'service', 
                 'booking_date', 'booking_time', 'status']
        read_only_fields = ['client', 'status']
        swagger_schema_fields = {
            "example": {
                "salon": 1,
                "staff": 1,
                "service": {
                    "name": "Стрижка",
                    "price": 1500
                },
                "booking_date": "2024-03-20",
                "booking_time": "14:30"
            }
        } 