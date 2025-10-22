# fastapi - Main class to create FastAPI application, HTTP exceptions for error handling
from fastapi import FastAPI, HTTPException
# SQLAlchemy - Work with database, classes to define structure of table
from sqlalchemy import create_engine, Column, Integer, String, Text, TIMESTAMP
# SQLAlchemy - Create base class for database models
from sqlalchemy.ext.declarative import declarative_base
# SQLAlchemy - Create session(connection) to interact with the database
from sqlalchemy.orm import sessionmaker
# Pydantic - Data validation and settings management for data from API using Python type annotations
from pydantic import BaseModel
# Typing - For type hints
from typing import Optional
# os - For working with environment variables
import os
# working with dates and times
from datetime import datetime

# Database connection settings from environment variables
try:
    DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@mariadb:3306/tasks_db")
except Exception as e:
    raise Exception(f"Error connecting to the db.\n {e}") from e

# Create database engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our classes definitions
Base = declarative_base()

# Define Task model for the database
class TaskDB(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True, nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(50), default="NEW", nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now, nullable=False)

# Define Pydantic model for creating Task
class TaskCreate(BaseModel):
    title: str
    description: str
    status: Optional[str] = "NEW"

# Define Pydantic model for updating Task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

# Define Pydantic model for Task response
class Task(BaseModel):
    task_id: int
    title: str
    description: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

# Initialize FastAPI app
app = FastAPI(title="Task Management API")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Task Management API"}

# Endpoint to get list of tasks with pagination and optional status filtering
@app.get("/tasks/", response_model=list[Task])
def read_tasks(status: Optional[str] = None):
    """
    Retrieve tasks from the database with pagination.
    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    db = SessionLocal()
    try:
        query = db.query(TaskDB)
        if status:
            query = query.filter(TaskDB.status == status)
        query = query.all()
        return query
    finally:
        db.close()

# Endpoint to get a specific task by ID
@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    """
    Retrieve a specific task by its ID.
    - **task_id**: The ID of the task to retrieve
    """
    db = SessionLocal()
    try:
        db_task = db.query(TaskDB).filter(TaskDB.task_id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        return db_task
    finally:
        db.close()

# Endpoint to create a new task
@app.post("/tasks/", response_model=Task, status_code=201)
def create_task(task_create: TaskCreate):
    """
    Create a new task in the database.
    - **task**: Task data to create
    """
    db = SessionLocal()
    try:
        db_task = TaskDB(**task_create.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    finally:
        db.close()

# Endpoint to update an existing task by ID
@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskUpdate):
    """
    Update an existing task in the database.
    - **task_id**: The ID of the task to update
    - **task**: Updated task data
    """
    db = SessionLocal()
    try:
        db_task = db.query(TaskDB).filter(TaskDB.task_id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        update_data = task_update.model_dump(exclude_unset=True)
        for var, value in update_data.items():
            if value is not None:
                setattr(db_task, var, value)
        db.commit()
        db.refresh(db_task)
        return db_task
    finally:
        db.close()

# Endpoint to delete a task by ID
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """
    Delete a task from the database.
    - **task_id**: The ID of the task to delete
    """
    db = SessionLocal()
    try:
        db_task = db.query(TaskDB).filter(TaskDB.task_id == task_id).first()
        if not db_task:
            raise HTTPException(status_code=404, detail="Task not found")
        db.delete(db_task)
        db.commit()
        return
    finally:
        db.close()

# Launch FastAPI (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
