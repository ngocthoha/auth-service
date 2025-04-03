# Authentication & Authorization Service

A microservice for handling authentication and authorization using FastAPI and JWT tokens with refresh token capabilities and role-based access control (RBAC).

## Features

- **Authentication:** OAuth2 with JWT tokens and refresh tokens
- **Authorization:** Role-based access control (RBAC)
- **User Management:** Create, read, update, and delete users with proper permission checks
- **Security:** Password hashing with bcrypt, token revocation

## Requirements

- Python 3.8+
- FastAPI
- SQLAlchemy
- PostgreSQL or SQLite

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the environment variables in `.env` file

## Running the service

```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Usage

### Authentication

1. Register a user (if admin) or use an existing user
2. Login to get access and refresh tokens:
   ```
   POST /api/v1/auth/login
   ```
3. Use the access token in the Authorization header:
   ```
   Authorization: Bearer <access_token>
   ```
4. When the access token expires, use the refresh token to get a new one:
   ```
   POST /api/v1/auth/refresh
   ```
5. To logout, revoke the refresh token:
   ```
   POST /api/v1/auth/logout
   ```

### User Management

- Create a user (admin only):
  ```
  POST /api/v1/users
  ```
- Get current user:
  ```
  GET /api/v1/users/me
  ```
- Update current user:
  ```
  PUT /api/v1/users/me
  ```
- List users (requires LIST permission):
  ```
  GET /api/v1/users
  ```
- Get user by ID (requires READ permission):
  ```
  GET /api/v1/users/{user_id}
  ```
- Update user (requires UPDATE permission):
  ```
  PUT /api/v1/users/{user_id}
  ```
- Delete user (requires DELETE permission):
  ```
  DELETE /api/v1/users/{user_id}
  ```

## Role-Based Access Control

The service implements RBAC with the following roles:
- **Admin:** Full access to all resources
- **User:** Limited access, can read but not modify most resources
- **Service:** Special role for service-to-service communication

## Database Migrations

This service uses SQLAlchemy models. For production, you might want to add Alembic for database migrations.