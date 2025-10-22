# Streamlit app.py file for Task Management Application
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(
    page_title="Web tasks management",
    page_icon=":memo:",
    layout="wide"
)

# Create app title and description
st.title("Task Management App")
st.markdown("---")
st.markdown("This is a simple Task Management application built with Streamlit and FastAPI.")
st.markdown("""
    ### Welcome to the Task Management App!

    This application allows you to manage your tasks efficiently.

    - **View Tasks**: See the list of your tasks with their details.
    - **Add Tasks**: Create new tasks and keep track of them.
    - **Update Tasks**: Modify existing tasks as needed.
    - **Delete Tasks**: Remove tasks that are no longer needed.

    ### Technologies Used:
    - **Frontend**: Streamlit (Python)
    - **Backend**: FastAPI (Python)
    - **Database**: MariaDB
    - **Orchestration**: Docker Compose

    Enjoy managing your tasks!
""")