from django.contrib import admin
from .models import Salon, Staff, Booking

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    search_fields = ('title', 'description', 'owner__phone_number')
    list_filter = ('created_at',)
    ordering = ('title',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'salon', 'created_at')
    list_filter = ('salon', 'created_at')
    search_fields = ('full_name', 'salon__title')
    ordering = ('salon', 'full_name')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'salon', 'staff', 'booking_date', 'booking_time', 'status')
    list_filter = ('status', 'booking_date', 'salon', 'staff')
    search_fields = ('client__phone_number', 'client__first_name', 'client__last_name', 
                    'salon__title', 'staff__full_name')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date', '-booking_time')
