# Salon Booking System

A mobile application for booking salon services. This project consists of a Django backend API and a React Native mobile app.

## Features

- Phone number authentication with OTP
- Salon listing and details
- Staff management
- Service booking system
- Working hours and availability management
- User profile management

## Backend Setup

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication
- `POST /api/users/send-otp/` - Send OTP to phone number
- `POST /api/users/verify-otp/` - Verify OTP and get JWT tokens
- `POST /api/users/update-profile/` - Update user profile

### Salons
- `GET /api/salons/` - List all salons
- `GET /api/salons/{id}/` - Get salon details
- `GET /api/salons/{id}/available_times/` - Get available booking times
- `POST /api/salons/` - Create new salon (admin only)

### Staff
- `GET /api/staff/` - List all staff members
- `GET /api/staff/{id}/` - Get staff details
- `POST /api/staff/` - Add new staff member (admin only)

### Bookings
- `GET /api/bookings/` - List user's bookings
- `POST /api/bookings/` - Create new booking
- `GET /api/bookings/{id}/` - Get booking details
- `PUT /api/bookings/{id}/` - Update booking status

## Development Notes

- For development, the OTP code is always "11111"
- JWT tokens are used for authentication
- CORS is enabled for all origins in development
- Media files are stored in the `media` directory
- Static files are collected in the `staticfiles` directory

## Mobile App Setup

The mobile app is built with React Native. To set it up:

1. Install dependencies:
```bash
cd mobile
npm install
```

2. Run the app:
```bash
# For iOS
npm run ios

# For Android
npm run android
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 