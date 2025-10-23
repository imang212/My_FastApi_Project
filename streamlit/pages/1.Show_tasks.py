# Streamlit page to show tasks from FastAPI backend
import streamlit as st
# Requests library to make HTTP requests
import requests
# OS library for environment variables
import os
from datetime import datetime

# FastAPI backend configuration URL from environment variable or default
API_URL = os.getenv("FASTAPI_URL", "http://fastapi:8000")

# Set Streamlit page configuration
st.set_page_config(page_title="Show Tasks", page_icon=":clipboard:", layout="wide")

# create page title
st.title("Task List")
# make horizontal line
st.markdown("---")

# Filter input for task status
col1, col2 = st.columns([1, 3])
with col1:
    # Dropdown to filter tasks by status
    filter_status = st.selectbox("Filter by Status", options=["ALL", "NEW", "IN_PROGRESS", "COMPLETED"], index=0, key="filter")

# mapping for status filter on the API query parameters
status_map = {
    "ALL": None,
    "NEW": "NEW",
    "COMPLETED": "COMPLETED"
}

# Function to fetch tasks from FastAPI backend
def fetch_tasks():
    try:
        # Prepare query parameters based on filter
        params = {}
        if status_map[filter_status]:
            params["status"] = status_map[filter_status]
        # Make GET request to fetch tasks
        response = requests.get(f"{API_URL}/tasks/", params=params)
        # Raise error for bad responses
        response.raise_for_status()
        # Return JSON response as list of tasks
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tasks: {e}")
        return []

# Function to create task display container
def create_task_container():
    tasks = fetch_tasks()
    if not tasks:
        st.info("No tasks found for the selected filter.")
    else:
        st.success(f"Fetched {len(tasks)} tasks.")
        # Display tasks in a table
        for task in tasks:
            # Convert created_at to readable format
            task['created_at_converted_date'] = datetime.fromisoformat(str(task["created_at"])).strftime("%d.%m.%Y at %H:%M")
            # Create a container for each task
            with st.container():
                # create columns for task details and action buttons
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    st.markdown(f"### **{task['title']}**")
                    if task['description']:
                        st.markdown(f"{task['description']}")
                    st.markdown(f"{task['created_at_converted_date']}*")

                with col2:
                    if task["status"] == "NEW":
                        st.markdown("**Ststus:** <p style='color:green;'>NEW</p>")
                    elif task["status"] == "COMPLETE":
                        st.markdown("**Status:** <p style='color:green;'>COMPLETE</p>")
                    else:
                        st.markdown("**Status:** <p style='color:orange;'>IN_PROGRESS</p>")
                with col3:
                    if task["status"] == "IN_PROGRESS":
                        if st.button("Hotovo", key=f"completed_{task['task_id']}"):
                            update_response = requests.put(
                                f"{API_URL}/tasks/{task['task_id']}",
                                json={"status": "COMPLETED"}
                            )
                            if update_response.status_code == 200:
                                st.success("Úkol označen jako hotový!")
                                st.rerun()
                            else:
                                st.error("Chyba při aktualizaci úkolu")
                    else:
                        if st.button("Obnovit", key=f"restore_{task['task_id']}"):
                            update_response = requests.put(
                                f"{API_URL}/tasks/{task['task_id']}",
                                json={"status": "IN_PROGRESS"}
                            )
                            if update_response.status_code == 200:
                                st.success("Úkol obnoven!")
                                st.rerun()
                            else:
                                st.error("Chyba při aktualizaci úkolu")

                with col4:
                    if st.button("Smazat", key=f"delete_{task['task_id']}"):
                        delete_response = requests.delete(f"{API_URL}/tasks/{task['task_id']}")
                        if delete_response.status_code == 204:
                            st.success("Úkol smazán!")
                            st.rerun()
                        else:
                            st.error("Chyba při mazání úkolu")
                st.markdown("---")

create_task_container()

# End of Streamlit page to show tasks from FastAPI backend
