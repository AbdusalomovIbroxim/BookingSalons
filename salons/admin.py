from django.contrib import admin
from django import forms
from django.utils.html import format_html
from .models import Salon, Staff, Booking, SalonPhoto
from django_json_widget.widgets import JSONEditorWidget

class WorkingHoursWidget(forms.Widget):
    template_name = 'admin/working_hours_widget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        if value:
            hours = value
        else:
            hours = {
                'mon': {'start_time': '08:00', 'end_time': '20:00'},
                'tue': {'start_time': '08:00', 'end_time': '20:00'},
                'wed': {'start_time': '08:00', 'end_time': '20:00'},
                'thu': {'start_time': '08:00', 'end_time': '20:00'},
                'fri': {'start_time': '08:00', 'end_time': '20:00'},
                'sat': {'start_time': '08:00', 'end_time': '20:00'},
                'sun': {'start_time': '08:00', 'end_time': '20:00'}
            }
        context['hours'] = hours
        return context

class SalonAdminForm(forms.ModelForm):
    working_hours = forms.JSONField(widget=WorkingHoursWidget())

    class Meta:
        model = Salon
        fields = '__all__'

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
    form = SalonAdminForm
    inlines = [SalonPhotoInline]
    list_display = ('title', 'owner', 'created_at', 'display_photos_count', 'display_working_hours')
    search_fields = ('title', 'description', 'owner__phone_number')
    list_filter = ('created_at',)
    ordering = ('title',)
    
    def display_photos_count(self, obj):
        return f"{obj.photos.count()} фото"
    display_photos_count.short_description = 'Количество фото'
    
    def display_working_hours(self, obj):
        if not obj.working_hours:
            return "Не указано"
        hours = obj.working_hours
        days = {
            'mon': 'Пн',
            'tue': 'Вт',
            'wed': 'Ср',
            'thu': 'Чт',
            'fri': 'Пт',
            'sat': 'Сб',
            'sun': 'Вс'
        }
        result = []
        for day, label in days.items():
            start = hours.get(day, {}).get('start_time', '-')
            end = hours.get(day, {}).get('end_time', '-')
            result.append(f"{label}: {start}-{end}")
        return format_html('<div style="white-space: pre-line">{}</div>', '\n'.join(result))
    display_working_hours.short_description = 'Время работы'

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
