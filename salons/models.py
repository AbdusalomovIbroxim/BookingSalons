from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import json

User = get_user_model()

class Salon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lon = models.DecimalField(max_digits=9, decimal_places=6)
    yandex_link = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_salons')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SalonPhoto(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='salon_photos/')
    order = models.PositiveIntegerField(default=0)
    is_main = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Фото салона'
        verbose_name_plural = 'Фотографии салона'

    def __str__(self):
        return f"Фото {self.order} для {self.salon.title}"

    def save(self, *args, **kwargs):
        if self.is_main:
            SalonPhoto.objects.filter(salon=self.salon, is_main=True).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

class Staff(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='staff')
    full_name = models.CharField(max_length=200)
    services = models.JSONField()  # List of services with prices
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.salon.title}"

    def get_services(self):
        return json.loads(self.services)

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
