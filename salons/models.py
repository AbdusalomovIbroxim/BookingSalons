from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import json

User = get_user_model()

class Salon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    photos = models.JSONField(default=list)  # Array of photo URLs
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lon = models.DecimalField(max_digits=9, decimal_places=6)
    yandex_link = models.URLField()
    working_hours = models.JSONField()  # Working hours for each day
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_salons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_working_hours(self):
        return json.loads(self.working_hours)

class Staff(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='staff')
    full_name = models.CharField(max_length=200)
    services = models.JSONField()  # List of services with prices
    working_shifts = models.JSONField()  # Working shifts for each day
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.salon.title}"

    def get_services(self):
        return json.loads(self.services)

    def get_working_shifts(self):
        return json.loads(self.working_shifts)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='bookings')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='bookings')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.JSONField()  # Selected service with price
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} - {self.client.username} at {self.salon.title}"

    class Meta:
        ordering = ['-booking_date', '-booking_time']
