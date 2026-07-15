FastAPI Task Manager
A modern REST API for task management with JWT authentication, built with FastAPI and PostgreSQL. This project demonstrates best practices in building scalable, secure, and maintainable RESTful APIs with Python.

📝 Description
FastAPI Task Manager is a robust backend service that provides a complete solution for task management applications. It implements industry-standard security practices, follows RESTful principles, and provides comprehensive documentation out of the box.

Key Features
Secure Authentication: JWT-based authentication system with password hashing and token expiration
Task Management: Full CRUD operations for tasks with user-specific access control
Database Integration: PostgreSQL database with SQLAlchemy ORM for efficient data management
Real-time Logging: Action tracking and monitoring through Firebase integration
API Documentation: Interactive API documentation with Swagger UI and ReDoc
Containerization: Docker support for easy deployment and development
Scalable Architecture: Modular design that's easy to extend and maintain
Use Cases
Task management applications
Project tracking systems
Backend for mobile applications
Learning resource for FastAPI and JWT implementation
Template for building secure REST APIs
Technical Highlights
Clean architecture with dependency injection
Comprehensive error handling
Input validation with Pydantic
Database migrations support
Environment-based configuration
Docker containerization
Automated API documentation
📋 Documentation
Changelog - Version history and changes
Future Improvements - Planned features and pending improvements
📋 Changelog
Para ver los cambios recientes y el historial de versiones, consulta el archivo CHANGELOG.md.

🚀 Features
🔐 JWT Authentication
👥 User Management (register, login)
✅ Task CRUD Operations
🗄️ PostgreSQL Database
📚 Automatic API Documentation (Swagger/OpenAPI)
📊 Action Logging in Firestore
🐳 Docker and Docker Compose Support
🛠️ Tech Stack
FastAPI - Modern, fast web framework
PostgreSQL - Robust relational database
SQLAlchemy - Python ORM
Pydantic - Data validation and serialization
JWT - Token-based authentication
Docker - Containerization and deployment
Firebase - Logging and monitoring
📋 Prerequisites
Python 3.11+
Docker and Docker Compose
PostgreSQL
Firebase Account (for Firestore)
📁 Project Structure
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Application configuration
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication functions
│   ├── deps.py              # FastAPI dependencies
│   ├── firestore_logger.py  # Firestore logging
│   └── routes/              # API routes
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       └── tasks.py         # Task routes
├── migrations/              # Database migration scripts
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker configuration
└── docker-compose.yml      # Docker Compose configuration
🚀 Getting Started
Clone the repository:
git clone https://github.com/2312-miguel/fastapi-task-manager.git
cd fastapi-task-manager
Create a .env file in the project root with the following variables:
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql://user:password@db:5432/dbname
FIREBASE_CREDENTIALS_PATH=/path/to/firebase-credentials.json
Start the services with Docker Compose:
docker-compose up -d
📚 API Usage
Authentication
Register a new user:
POST /auth/register
Content-Type: application/json

{
    "email": "user@example.com",
    "username": "username",
    "password": "password123"
}
Login:
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=password123
Tasks
Create a task:
POST /tasks
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "My task",
    "description": "Task description",
    "done": false
}
List tasks:
GET /tasks
Authorization: Bearer <token>
Get specific task:
GET /tasks/{task_id}
Authorization: Bearer <token>
📖 Documentation
API documentation is available at:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc
💻 Development
Install Dependencies
pip install -r requirements.txt
Run Tests
pytest
Run Linting
flake8
🐳 Docker Commands
Build Image
docker-compose build
Start Services
docker-compose up -d
View Logs
docker-compose logs -f
Stop Services
docker-compose down
🔒 Security Features
JWT Authentication
Password Hashing with bcrypt
SQL Injection Protection
Input Validation with Pydantic
Secure Headers Configuration
