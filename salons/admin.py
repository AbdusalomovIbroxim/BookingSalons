from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Salon, Staff, Booking, SalonPhoto

class SalonPhotoInline(admin.TabularInline):
    model = SalonPhoto
    extra = 1
    fields = ('image', 'order', 'is_main', 'preview')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "Нет изображения"
    preview.short_description = 'Предпросмотр'

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    inlines = [SalonPhotoInline]
    list_display = ('title', 'owner', 'created_at', 'display_photos_count')
    search_fields = ('title', 'description', 'owner__phone_number')
    list_filter = ('created_at',)
    ordering = ('title',)
    
    def display_photos_count(self, obj):
        return f"{obj.photos.count()} фото"
    display_photos_count.short_description = 'Количество фото'

@admin.register(SalonPhoto)
class SalonPhotoAdmin(admin.ModelAdmin):
    list_display = ('salon', 'preview', 'order', 'is_main', 'created_at')
    list_filter = ('salon', 'is_main', 'created_at')
    search_fields = ('salon__title',)
    ordering = ('salon', 'order')
    readonly_fields = ('preview',)

    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.image.url)
        return "Нет изображения"
    preview.short_description = 'Предпросмотр'

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
