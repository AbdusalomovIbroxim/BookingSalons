from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Salon, Staff, Booking
from django_json_widget.widgets import JSONEditorWidget

class SalonAdminForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = '__all__'
        widgets = {
            'working_hours': JSONEditorWidget(
                options={
                    'modes': ['tree', 'view'],
                    'mode': 'tree',
                    'schema': {
                        'type': 'object',
                        'properties': {
                            'mon': {'type': 'object', 'properties': {'start_time': {'type': 'string'}, 'end_time': {'type': 'string'}}},
                            'tue': {'type': 'object', 'properties': {'start_time': {'type': 'string'}, 'end_time': {'type': 'string'}}},
                            'wed': {'type': 'object', 'properties': {'start_time': {'type': 'string'}, 'end_time': {'type': 'string'}}},
                            'thu': {'type': 'object', 'properties': {'start_time': {'type': 'string'}, 'end_time': {'type': 'string'}}},
                            'fri': {'type': 'object', 'properties': {'start_time': {'type': 'string'}, 'end_time': {'type': 'string'}}},
                            'sat': {'type': 'object', 'properties': {'start_time': {'type': 'string'}, 'end_time': {'type': 'string'}}},
                            'sun': {'type': 'object', 'properties': {'start_time': {'type': 'string'}, 'end_time': {'type': 'string'}}}
                        }
                    }
                }
            ),
            'photos': JSONEditorWidget(
                options={
                    'modes': ['tree', 'view'],
                    'mode': 'tree',
                    'schema': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'minItems': 1,
                        'maxItems': 14
                    }
                }
            )
        }

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    form = SalonAdminForm
    list_display = ('title', 'owner', 'created_at', 'display_photos_count', 'display_working_hours')
    search_fields = ('title', 'description', 'owner__phone_number')
    list_filter = ('created_at',)
    ordering = ('title',)
    
    def display_photos_count(self, obj):
        photos = obj.photos if isinstance(obj.photos, list) else []
        return f"{len(photos)} фото"
    display_photos_count.short_description = 'Количество фото'
    
    def display_working_hours(self, obj):
        if not obj.working_hours:
            return "Не указано"
        hours = obj.working_hours
        return format_html(
            '<div style="white-space: pre-line">'
            'Пн: {} - {}\n'
            'Вт: {} - {}\n'
            'Ср: {} - {}\n'
            'Чт: {} - {}\n'
            'Пт: {} - {}\n'
            'Сб: {} - {}\n'
            'Вс: {} - {}'
            '</div>',
            hours.get('mon', {}).get('start_time', '-'),
            hours.get('mon', {}).get('end_time', '-'),
            hours.get('tue', {}).get('start_time', '-'),
            hours.get('tue', {}).get('end_time', '-'),
            hours.get('wed', {}).get('start_time', '-'),
            hours.get('wed', {}).get('end_time', '-'),
            hours.get('thu', {}).get('start_time', '-'),
            hours.get('thu', {}).get('end_time', '-'),
            hours.get('fri', {}).get('start_time', '-'),
            hours.get('fri', {}).get('end_time', '-'),
            hours.get('sat', {}).get('start_time', '-'),
            hours.get('sat', {}).get('end_time', '-'),
            hours.get('sun', {}).get('start_time', '-'),
            hours.get('sun', {}).get('end_time', '-')
        )
    display_working_hours.short_description = 'Время работы'

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
