# Streamlit page to show tasks from FastAPI backend
import streamlit as st
# Requests library to make HTTP requests
import requests
# OS library for environment variables
import os

# FastAPI backend configuration URL from environment variable or default
API_URL = os.getenv("FASTAPI_API_URL", "http://fastapi:8000")

# Set Streamlit page configuration
st.set_page_config(page_title="Add Task", page_icon=":heavy_plus_sign:", layout="wide")

# create page title
st.title("Add New Task")

# make horizontal line
st.markdown("---")

def create_task_form():
    with st.form(key="add_task_form"):
        title = st.text_input(
            "Task title *",
            placeholder="Buy groceries, Complete project report, etc.",
            help="Field is required.",
            max_chars=255
        )
        description = st.text_area(
            "Task Description",
            placeholder="Provide more details about the task...",
            help="Field is required.",
            height=150
        )
        status = st.selectbox("Task Status", options=["NEW", "IN_PROGRESS", "COMPLETED"], index=0)

        col1, col2 = st.columns([1, 4])
        with col1:
            submit_button = st.form_submit_button(label="Add Task")

    # Handle form submission
    if submit_button:
        if not title.strip():
            st.error("Please enter a task title.")
        else:
            #
            try:
                # Prepare task data
                task_data = {
                    "title": title,
                    "description": description,
                    "status": status
                }
                # Send POST request to FastAPI backend to add new task
                response = requests.post(f"{API_URL}/tasks/", json=task_data)
                if response.status_code == 201:
                    st.success("Task added successfully!")
                    st.balloons()
                    # Show created task details
                    created_task = response.json()
                    st.info(f"""
                        **Task created:**
                        - Name: {created_task['title']}
                        - Description: {created_task['description'] or 'Bez popisu'}
                        - Status: {created_task['status']}
                    """)
                    st.success("Task added successfully!")
                else:
                    st.error(f"Error adding task: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error adding task: {e}")
    st.markdown("---")
    # Nabídka přidat další úkol nebo přejít na seznam
    col1, col2 = st.columns(2)
    with col1:
        if st.button(label="Add another task"):
            st.switch_page("pages/1.Show_tasks.py")

create_task_form()
st.markdown("---")
st.markdown("""
    # Instructions
    Use this form to add new tasks to your task management system.
    Fill in the task title, description, and select the status.
    After submitting, the task will be added to the FastAPI backend and you can view all tasks on the 'Show Tasks' page.
""")