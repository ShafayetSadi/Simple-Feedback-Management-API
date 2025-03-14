# Simple-Feedback-Management-API

A **Django REST API** for managing user feedback with authentication, CRUD operations, and role-based access control.

---

## 🌟 Features

- **JWT Authentication** (Login & Register)
- **Role-based Access Control** (Admin & User)
- **CRUD Operations for Feedback**
- **Create**: Users can submit feedback
- **Read**: Users can view their feedback. Admins can view all feedback
- **Update**: Users can update their feedback. Admins can update all feedback
- **Delete**: Users can delete their feedback. Admins can delete all feedback
- **RESTful API with Django REST Framework**
- **Comprehensive Unit Tests**

---

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:

- **Python 3.12+**
- **Django**
- **uv**
- **PostgreSQL or SQLite (Default)**

### Installation

Clone the repository and navigate into the project directory:

```sh
git clone https://github.com/yourusername/feedback-management-api.git
cd feedback-management-api
```

Set up a virtual environment and install the dependencies:

```sh
uv sync
```

Set up environment variables:

```sh
cp .env.example .env # Adjust the values in the .env file
```

Run the migrations:

```sh
uv run python manage.py migrate
```

Populate the database with sample data:

```sh
uv run python manage.py populate_feedback
```

Create a superuser:

```sh
uv run python manage.py createsuperuser
```

Run the development server:

```sh
uv run python manage.py runserver
```

Access the API at `http://127.0.0.1:8000/api/`

---

## 📌 API Endpoints

### Authentication

| Method | Endpoint           | Description             |
|--------|--------------------|-------------------------|
| POST   | /api/register/     | Register a new user     |
| POST   | /api/login/        | Login and get JWT token | 
| POST   | /api/token/refresh | Refresh JWT token       |

### Feedback Management

| Method | Endpoint          | Access             | Description           |
|--------|-------------------|--------------------|-----------------------|
| GET    | /api/feedback/    | Admin Only         | Get all feedback      |
| POST   | /api/feedback/    | Authenticated User | Create a new feedback |
| GET    | /api/feedback/id/ | User               | Get feedback by ID    |
| PUT    | /api/feedback/id/ | Owner/Admin        | Update feedback by ID |
| DELETE | /api/feedback/id/ | Owner/Admin        | Delete feedback by ID |

## 📌 Example Usage

### Register a new user

```sh
curl -X POST http://127.0.0.1:8000/api/register/ \
     -H "Content-Type: application/json" \
     -d '{"username": "johndoe", "password": "securepassword", "email": "john@example.com"}'
```

### Login and get JWT token

```sh
curl -X POST http://127.0.0.1:8000/api/login/ \
     -H "Content-Type: application/json" \
     -d '{"username": "johndoe", "password": "securepassword"}'
```

Response:

```json
{
  "access": "your_jwt_access_token",
  "refresh": "your_jwt_refresh_token"
}
```

### Create a new feedback

```sh
curl -X POST http://127.0.0.1:8000/api/feedback/ \
     -H "Authorization: Bearer your_jwt_access_token" \
     -H "Content-Type: application/json" \
     -d '{"title": "Bug in login", "description": "Login button is not working", "category": "bug report"}'
```

### Get all feedback (Admin Only)

```sh
curl -X GET http://127.0.0.1:8000/api/feedback/ \
     -H "Authorization: Bearer admin_jwt_token"
```

### Get feedback by ID (User)

```sh
curl -X GET http://127.0.0.1:8000/api/feedback/1/
```

### Update feedback by ID (Owner/Admin)

```sh
curl -X PUT http://127.0.0.1:8000/api/feedback/1/ \
     -H "Authorization: Bearer your_jwt_access_token" \
     -H "Content-Type: application/json" \
     -d '{"title": "Updated Title", "status": "resolved"}'
```

---

## 🧪 Running Tests

Run the unit tests with the following command:

```sh
uv run python manage.py test
```

---

## 🤝 Contribution Guidelines

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feat/some-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add some feature'`)
5. Push to the branch (`git push origin feat/some-feature`)
6. Create a new Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

