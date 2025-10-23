# Web Task Manager
A modern web application for managing personal tasks built on microservice architecture using Docker containers.

## About the Project
Web Task Manager is a fully functional application for managing personal tasks (TODO list) that demonstrates modern web application development with separation of frontend, backend, and database into standalone Docker containers.

### Key Features
- **View Tasks** - Clear list of all tasks with filtering options
- **Add Task** - Form for creating new tasks with title and description
- **Change Status** - Mark tasks as NEW/IN_PROGRESS/COMPLETE with a single click
- **Delete Task** - Permanently remove tasks from the database
- **Color Coding** - Visual distinction between completed and new tasks
- **Timestamps** - Automatic recording of task creation time

## Architecture
The application uses a **microservice architecture** with three main components:

```
┌─────────────────┐
│   Streamlit     │ ← Frontend (Port 8501)
│   (Python)      │
└────────┬────────┘
         │ HTTP REST API
┌────────▼────────┐
│    FastAPI      │ ← Backend (Port 8000)
│   (Python)      │
└────────┬────────┘
         │ SQL
┌────────▼────────┐
│    MariaDB      │ ← Database (Port 3306)
│   (MySQL)       │
└─────────────────┘
```

### Components
#### **Frontend - Streamlit**
- Modern web user interface
- Responsive design
- Interactive forms and buttons
- Real-time data updates

#### **Backend - FastAPI**
- RESTful API with automatic documentation
- Asynchronous request processing
- Data validation using Pydantic
- ORM mapping using SQLAlchemy

#### **Database - MariaDB**
- Relational database for persistent data storage
- Automatic schema initialization
- Persistent data storage

## Technologies:
### Backend
- **FastAPI** 0.104.1 - Modern Python web framework
- **SQLAlchemy** 2.0.23 - SQL toolkit and ORM
- **PyMySQL** 1.1.0 - MySQL database connector
- **Pydantic** 2.5.0 - Data validation and settings
- **Uvicorn** 0.24.0 - ASGI server

### Frontend
- **Streamlit** 1.28.1 - Framework for building data applications
- **Requests** 2.31.0 - HTTP library for API communication

### Database & Infrastructure
- **MariaDB** latest - Relational database management system
- **Docker** - Application containerization
- **Docker Compose** - Multi-container orchestration

## Installation and Running
### Prerequisites
- Docker Desktop installed on your system
- Docker Compose (usually part of Docker Desktop)
- Git (for cloning the repository)

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/web-task-manager.git
cd web-task-manager
```

### Step 2: Start the Application
```bash
docker-compose up --build
```

This command will:
- Download necessary Docker images
- Build containers for frontend, backend, and database
- Start all services

### Step 3: Open the Application
After successful startup, open in your browser:
- **Streamlit UI**: http://localhost:8501
- **FastAPI Documentation**: http://localhost:8000/docs
- **FastAPI Redoc**: http://localhost:8000/redoc

## Project Structure
```
My_FastApi_Project/
├── docker-compose.yml          # Docker container orchestration
│
├── sql/
│   └── init.sql               # SQL initialization script
│
├── fastapi/
│   ├── Dockerfile             # Docker configuration for backend
│   ├── requirements.txt       # Backend Python dependencies
│   └── main.py               # FastAPI application and API endpoints
│
└── streamlit/
    ├── Dockerfile             # Docker configuration for frontend
    ├── requirements.txt       # Frontend Python dependencies
    ├── app.py               # Main application page
    └── pages/
        ├── 1.Show_tasks.py   # Task list page
        └── 2.Add_task.py      # Add task page
```

## API Endpoints
The backend provides the following REST API endpoints:

### GET `/tasks/`
Returns a list of all tasks (or filtered by status)

**Query parameters:**
- `status` (optional) - Filter by status (`new` or `done`)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "status": "new",
    "created_at": "2025-10-22T13:20:05"
  }
]
```

### POST `/tasks/`
Creates a new task

**Request body:**
```json
{
  "title": "New task",
  "description": "Task description",
  "status": "new"
}
```

### PUT `/tasks/{task_id}`
Updates an existing task

**Request body:**
```json
{
  "status": "done"
}
```

### DELETE `/tasks/{task_id}`
Deletes a task by ID

**Response:** 204 No Content

## Database Schema
### Table `tasks_db`
| Column | Type | Description |
|---------|-----|-------|
| `task_id` | INT (PK, AUTO_INCREMENT) | Unique task identifier |
| `title` | VARCHAR(255) NOT NULL | Task title |
| `description` | TEXT | NOT NULL | Detailed task description |
| `status` | VARCHAR(50) DEFAULT 'NEW' | Task status (NEW/IN_PROGRESS/COMPLETE) | NOT NULL
| `created_at` | TIMESTAMP | Task creation time | NOT NULL

## Docker Configuration
### Services

**db** - MariaDB database
- Port: 3306
- Volume: Persistent data storage

**fastapi** - Backend API
- Port: 8000
- Depends on: db (waits for database availability)
- Auto-reload: Enabled for development

**streamlit** - Frontend UI
- Port: 8501
- Depends on: fastapi
- Environment: Automatic API URL configuration

### Data Persistence
Data is stored in the Docker volume `db_data`, which means:
- Data persists through container restarts
- Data is isolated from the host system
- Data is **deleted** with `docker-compose down -v`

## Stopping the Application
### Standard stop (preserves data)
```bash
docker-compose down
```

### Stop including data deletion
```bash
docker-compose down -v
```

### Restart individual service
```bash
docker-compose restart fastapi
docker-compose restart streamlit
```

## Development and Debugging
### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f fastapi
docker-compose logs -f streamlit
docker-compose logs -f db
```

### Access container
```bash
# Bash in FastAPI container
docker-compose exec fastapi bash

# Bash in Streamlit container
docker-compose exec streamlit bash

# MySQL client in DB container
docker-compose exec db mysql -u uzivatel -p ukoly_db
```

### Hot Reload
Both applications (FastAPI and Streamlit) support **automatic reload** when code changes:
- **FastAPI**: Uses `--reload` flag that detects changes in `main.py`
- **Streamlit**: Automatically detects changes in Python files

Simply edit a file and changes will take effect immediately (may need to refresh the page in browser).

## Possible Extensions
The project can be extended with the following features:
- **Edit Tasks** - Ability to modify title and description of existing tasks
- **Due Date** - Add `due_date` field for deadlines
- **Task Priority** - Mark importance (high/medium/low)
- **Categories** - Organize tasks into categories
- **Search** - Full-text search in tasks
- **User Accounts** - Authentication and separate tasks by user
- **Data Export** - Export tasks to CSV/JSON
- **Notifications** - Email alerts for approaching deadlines
- **Dark Mode** - Dark theme for Streamlit UI
- **API Rate Limiting** - Protection against API abuse
- **Unit Tests** - Automated code testing
- **CI/CD Pipeline** - Automatic deployment

## How to Contribute
1. Fork this repository
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## Troubleshooting
### Containers won't start
```bash
# Check if another application is already using the ports
docker-compose down
docker-compose up --build
```

### Error "Table doesn't exist"
```bash
# Delete volumes and fresh start
docker-compose down -v
docker-compose up --build
```

### Frontend can't connect to backend
- Check that all containers are running: `docker-compose ps`
- Check logs: `docker-compose logs fastapi`

### Database is not available
- Wait for health check (may take 10-30 seconds)
- Check logs: `docker-compose logs db`

