from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Salon, Staff, Booking, SalonPhoto
from .serializers import SalonSerializer, StaffSerializer, BookingSerializer, SalonPhotoSerializer
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# Create your views here.

class SalonViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления салонами.
    """
    queryset = Salon.objects.all()
    serializer_class = SalonSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'])
    def staff(self, request, pk=None):
        salon = self.get_object()
        staff = Staff.objects.filter(salon=salon)
        serializer = StaffSerializer(staff, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        salon = self.get_object()
        bookings = Booking.objects.filter(salon=salon)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

class StaffViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления персоналом салона.
    """
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Staff.objects.filter(salon__owner=self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления бронированиями.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(client=self.request.user)

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        booking = self.get_object()
        if booking.status == 'pending':
            booking.status = 'confirmed'
            booking.save()
            return Response({'status': 'confirmed'})
        return Response({'error': 'Booking cannot be confirmed'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()
            return Response({'status': 'cancelled'})
        return Response({'error': 'Booking cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)
