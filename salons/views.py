from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Salon, Staff, Booking
from .serializers import SalonSerializer, StaffSerializer, BookingSerializer
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.

class SalonViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления салонами.
    """
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def available_times(self, request, pk=None):
        """
        Получить доступное время для бронирования в салоне.
        """
        salon = self.get_object()
        date = request.query_params.get('date')
        staff_id = request.query_params.get('staff_id')
        
        if not date:
            return Response({'error': 'Date parameter is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return Response({'error': 'Invalid date format'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Get staff member if specified
        staff = None
        if staff_id:
            staff = get_object_or_404(Staff, id=staff_id, salon=salon)
        else:
            staff = salon.staff.first()

        if not staff:
            return Response({'error': 'No staff available'}, 
                          status=status.HTTP_404_NOT_FOUND)

        # Get working hours for the day
        working_hours = salon.get_working_hours()
        day_name = date.strftime('%a').lower()
        if day_name not in working_hours:
            return Response({'error': 'Salon is closed on this day'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Get staff shifts
        staff_shifts = staff.get_working_shifts()
        if day_name not in staff_shifts:
            return Response({'error': 'Staff is not working on this day'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        # Get existing bookings
        existing_bookings = Booking.objects.filter(
            salon=salon,
            staff=staff,
            booking_date=date,
            status__in=['pending', 'confirmed']
        ).values_list('booking_time', flat=True)

        # Generate available time slots
        start_time = datetime.strptime(staff_shifts[day_name]['start_time'], '%H:%M')
        end_time = datetime.strptime(staff_shifts[day_name]['end_time'], '%H:%M')
        current_time = start_time
        available_times = []

        while current_time < end_time:
            time_str = current_time.strftime('%H:%M')
            if time_str not in existing_bookings:
                available_times.append(time_str)
            current_time += timedelta(minutes=30)  # 30-minute slots

        return Response({'available_times': available_times})

class StaffViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления персоналом салона.
    """
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        salon_id = self.request.query_params.get('salon_id')
        if salon_id:
            return Staff.objects.filter(salon_id=salon_id)
        return Staff.objects.all()

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления бронированиями.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Booking.objects.none()
            
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(client=user)
