# Courier Management System — Backend API

## 📄 Project Overview
A scalable RESTful backend API for a Courier Management System. The system supports multiple roles and allows users to place and track orders, delivery men to manage assigned orders, and admins to manage the entire system.

### **Features**
- JWT-based authentication (register, login, profile update)
- Role-based access: Admin, Delivery Man, User
- Order management (create, assign, update, track)
- Stripe payment integration 

## 👥 Roles
| Role         | Permissions                                                                 |
|--------------|-----------------------------------------------------------------------------|
| Admin        | Full access: manage users, orders, assign delivery men                      |
| Delivery Man | View/update only their assigned orders status                               |
| User         | Register, login, create orders, view/track own orders (pending/delivered/complete) |

## 🔑 Authentication
- JWT-based authentication
- User registration and login
- Profile update

## 📦 Order Management
- Users create/view their own orders and check status
- Delivery men view/update only their assigned orders
- Admin views all orders and assigns delivery men

## 💳 Payment
- Users pay for delivery via Stripe 

## 🔗 Relation Diagram
> **Embed your ERD image here**

## 🔗 Links
- **Live API URL:** [LIVE_API_URL_HERE](https://courier-management-system-backend-api-53k6.onrender.com)
- **Postman Collection:** [Postman Collection](docs/Courier-Service.postman_collection.json)



## 📝 API Endpoints
### Accounts
- `POST /api/v1/auth/register/` — Register new user
- `POST /api/v1/auth/login/` — Login
- `GET /api/v1/auth/profile/` — Get user profile
- `PUT /api/v1/auth/profile/` — Update user profile

### Orders
- `POST /api/v1/orders/` — Create order (User)
- `GET /api/v1/orders/` — List own orders (User), all orders (Admin), assigned orders(Delivery Man)
- `GET /api/v1/orders/{id}/` — Get order details
- `PUT /api/v1/orders/{id}/` — Update order (Delivery Man/Admin)

### Payments
- `POST /api/v1/payments/create-checkout-session/` — Make payment (Stripe)
- `GET /api/v1/payments/success/` —  Success Page (Stripe)
- `GET /api/v1/payments/failed/` —  Failed Page (Stripe)
