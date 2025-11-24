# Farmo Server - Backend API

Django REST API for Farmo agricultural marketplace system.

## Setup

1. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure environment**
```bash
copy .env.example .env
# Edit .env with your database credentials
```

4. **Setup database**
- Create PostgreSQL database named `farmo_db`
- Run the SQL script from `Doc/SQL.txt` to create tables

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Run server**
```bash
python manage.py runserver
```

Server runs at: http://localhost:8000

## API Endpoints

### Authentication
- POST `/api/auth/register/farmer/` - Register farmer
- POST `/api/auth/register/consumer/` - Register consumer
- POST `/api/auth/login/farmer/` - Farmer login
- POST `/api/auth/login/consumer/` - Consumer login
- POST `/api/auth/login/admin/` - Admin login

### Products
- GET `/api/products/` - List all products
- POST `/api/products/` - Create product (auth required)
- GET `/api/products/{id}/` - Get product details
- PUT `/api/products/{id}/` - Update product (auth required)
- DELETE `/api/products/{id}/` - Delete product (auth required)
- GET `/api/products/search/?category=&organic=&search=` - Search products

### Orders
- GET `/api/orders/` - List orders (auth required)
- POST `/api/orders/` - Create order (auth required)
- GET `/api/orders/{id}/` - Get order details (auth required)

### Ratings
- POST `/api/farmer-ratings/` - Rate farmer (auth required)
- POST `/api/product-ratings/` - Rate product (auth required)

### Verification
- GET `/api/verifications/` - List verifications (auth required)
- POST `/api/verifications/{id}/approve/` - Approve farmer (auth required)

## Admin Panel
Access at: http://localhost:8000/admin
