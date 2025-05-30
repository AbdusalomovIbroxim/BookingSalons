"""
URL configuration for BookingSalons project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework import routers
from salons.views import SalonViewSet, StaffViewSet, BookingViewSet
from users.views import SendOTPView, VerifyOTPView, UpdateProfileView

# Create a router and register our viewsets with it
router = routers.DefaultRouter()
router.register(r'salons', SalonViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'bookings', BookingViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Salon Booking API",
        default_version='v1',
        description="""
        API для системы бронирования салонов красоты.
        
        ## Основные возможности:
        - Авторизация по номеру телефона с OTP
        - Управление салонами
        - Управление персоналом
        - Система бронирования
        - Управление профилем пользователя
        
        ## Аутентификация
        Для доступа к защищенным эндпоинтам используйте JWT токен в заголовке:
        ```
        Authorization: Bearer <token>
        ```
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@salonbooking.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('api/', include(router.urls)),
        path('api/users/', include('users.urls')),
    ],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/users/', include('users.urls')),
    
    # Swagger URLs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
