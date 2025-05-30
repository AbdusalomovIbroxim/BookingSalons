from rest_framework import serializers
from .models import Salon, Staff, Booking
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'first_name', 'last_name']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ['id', 'salon', 'full_name', 'services', 'working_shifts']
        swagger_schema_fields = {
            "example": {
                "salon": 1,
                "full_name": "Анна Петрова",
                "services": ["Стрижка", "Окрашивание", "Укладка"],
                "working_shifts": {
                    "mon": {"start_time": "09:00", "end_time": "18:00"},
                    "wed": {"start_time": "09:00", "end_time": "18:00"},
                    "fri": {"start_time": "09:00", "end_time": "18:00"}
                }
            }
        }

class SalonSerializer(serializers.ModelSerializer):
    staff = StaffSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Salon
        fields = ['id', 'title', 'description', 'photos', 'location_lat', 
                 'location_lon', 'yandex_link', 'working_hours', 'owner', 'staff']
        read_only_fields = ['owner']
        swagger_schema_fields = {
            "example": {
                "title": "Салон красоты 'Элегант'",
                "description": "Салон красоты с полным спектром услуг",
                "photos": ["https://example.com/photo1.jpg"],
                "location_lat": 55.7558,
                "location_lon": 37.6173,
                "yandex_link": "https://yandex.ru/maps/...",
                "working_hours": {
                    "mon": {"start_time": "09:00", "end_time": "21:00"},
                    "tue": {"start_time": "09:00", "end_time": "21:00"},
                    "wed": {"start_time": "09:00", "end_time": "21:00"},
                    "thu": {"start_time": "09:00", "end_time": "21:00"},
                    "fri": {"start_time": "09:00", "end_time": "21:00"},
                    "sat": {"start_time": "10:00", "end_time": "20:00"},
                    "sun": {"start_time": "10:00", "end_time": "18:00"}
                }
            }
        }

class BookingSerializer(serializers.ModelSerializer):
    salon = SalonSerializer(read_only=True)
    staff = StaffSerializer(read_only=True)
    client = UserSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'salon', 'staff', 'client', 'service', 'booking_date', 'booking_time', 'status']
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