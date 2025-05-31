from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'salon', 'staff', 'service', 'booking_date', 'status')
    list_filter = ('status', 'booking_date', 'salon', 'staff')
    search_fields = ('user__phone_number', 'user__first_name', 'user__last_name', 
                    'salon__name', 'staff__user__first_name', 'staff__user__last_name',
                    'service')
    date_hierarchy = 'booking_date'
    ordering = ('-booking_date',)
