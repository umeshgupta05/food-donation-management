# Food Donation Management System

A Django-based web application for managing food donations between donors (event organizers, hotels, individuals) and receivers (orphanages, NGOs, trusts).

## Features

- User registration with roles (Donor, Receiver, Admin)
- Donor dashboard for managing donations
- Receiver dashboard for claiming available donations
- Admin panel for managing users, verifying NGOs, and monitoring activities
- Donation posting, browsing, and claiming system
- Expiry tracking for food items

## Technology Stack

- Backend: Django (Python)
- Database: SQLite (development) / PostgreSQL (production)
- Frontend: Bootstrap 5, HTML, CSS, JavaScript
- Authentication: Django built-in authentication system with custom user model

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/food-donation-management.git
cd food-donation-management
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit `http://127.0.0.1:8000/` in your browser.

## Usage

- **As a Donor**: Register as a donor, add donations, track their status
- **As a Receiver**: Register as a receiver (NGO), browse available donations, claim them
- **As an Admin**: Approve/reject NGO registrations, monitor system activities

## License

[MIT License](LICENSE)
