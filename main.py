import streamlit as st
from multiapp import MultiApp
import home, employees, managers

# Set page parameters
st.set_page_config(page_title='Thinking Machines Exam',layout="wide")

app = MultiApp()

# Sidebar 
st.sidebar.markdown("""
# 🤖 HuRMI 
The Human Resource Management Interface aims to extract insight and information from the dataset provided by the company.
""")

app.add_app("Home", home.app)
app.add_app("Employees", employees.app)
app.add_app("Managers", managers.app)

app.run()


    