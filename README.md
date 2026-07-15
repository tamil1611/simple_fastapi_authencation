FastAPI Task Manager API
Secure task manager REST API built with FastAPI, SQLite, SQLAlchemy, Pydantic, bcrypt password hashing and JWT authentication.

Features
User signup, login and profile API
JWT protected task APIs
User-specific task ownership
Task CRUD with validation
Task search, status filter and pagination
Swagger UI customization with saved authorization
Docker support
Pytest API tests
Project Structure
app/
  api/
    deps.py
    routes/
      auth.py
      tasks.py
  core/
    config.py
    security.py
  crud/
    tasks.py
    users.py
  db/
    base.py
    init_db.py
    session.py
  models/
    task.py
    user.py
  schemas/
    auth.py
    common.py
    task.py
    user.py
main.py
tests/
postman/
Setup
python -m venv venv
.\venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
Update SECRET_KEY in .env with a long random value.

Run
python -m uvicorn main:app --reload
Open:

Swagger UI: http://127.0.0.1:8000/docs
ReDoc: http://127.0.0.1:8000/redoc
API Endpoints
Method	Endpoint	Auth	Description
POST	/auth/signup	No	Register user
POST	/auth/login	No	Login and get JWT token
GET	/auth/me	Yes	Get logged-in user
POST	/tasks	Yes	Add task
GET	/tasks	Yes	View logged-in user's tasks
GET	/tasks/{task_id}	Yes	View one task
PUT	/tasks/{task_id}	Yes	Update task
DELETE	/tasks/{task_id}	Yes	Delete task
GET /tasks supports:

status=Pending or status=Completed
search=keyword
skip=0
limit=20
Example Payloads
Signup:

{
  "full_name": "tamilselvi t",
  "email": "tamil@example.com",
  "password": "StrongPassword@123"
}
Login:

{
  "email": "tamil@example.com",
  "password": "StrongPassword@123"
}
Create task:

{
  "title": "Complete authentication assignment",
  "description": "Implement JWT authentication using FastAPI",
  "status": "Pending"
}
Use the login response token in Swagger's Authorize button as a bearer token.

Tests
pytest
Docker
docker build -t fastapi-task-manager .
docker run --env-file .env -p 8000:8000 fastapi-task-manager
Submission Documentation
Scrum master review notes and API evidence screenshots are available in:

docs/SCRUM_MASTER_UPDATE.md
Notes
If an old unauthenticated tasks table exists, the app preserves it by renaming it to tasks_legacy_YYYYMMDDHHMMSS and creates the new user-specific schema.

API screenshots can be kept in the screenshort/ folder, and the sample Postman collection is available at postman/task-manager.postman_collection.json.
