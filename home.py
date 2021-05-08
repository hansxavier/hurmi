import streamlit as st
import pandas as pd
import numpy as np

def app():
    # Read Data
    checkins = pd.read_csv('ese-l1-exam-checkins-dump.csv')
    checkins['date'] = pd.to_datetime(checkins['date'], format='%Y-%m-%d')  # Convert str to DateType

    st.title('Welcome to the Employee Check-In Dashboard!')
    st.markdown('''
    This application aims to assist Human Resource personnel with easy to understand information!
    Please use the Navigation bar on the left to get started with the application.
    ''')

    # Initial insights from the dataset
    stats = st.beta_container()
    with stats:
        st.title("Currently you have tracked...")
        dates, projects, managers, users = st.beta_columns(4)
        with dates:
            st.title(str(checkins['date'].nunique()))
            st.markdown('number of days logged.')
        with projects:
            st.title(str(checkins['project_id'].nunique()))
            st.markdown('unique projects')
        with managers:
            st.title(str(checkins['manager_id'].nunique()))
            st.markdown('number of managers')
        with users:
            st.title(str(checkins['user_id'].nunique()) )
            st.markdown('unique employees')
    
    today = st.beta_container()
    today_date = checkins['date'].iloc[-1]
    with today:
        st.title("Our last log was on " + str(today_date))
        st.markdown('Today your company has tracked...')
        today_data = checkins.loc[checkins['date'] == today_date]

        emp_t, proj_t, hours_t = st.beta_columns(3)
        with emp_t:
            st.title(str(today_data['user_id'].nunique()))
            st.markdown('Employees Checked-in')
        with proj_t: 
            st.title(str(today_data['project_id'].nunique()))
            st.markdown('Projects Logged')
        with hours_t:
            st.title(str(("%.1f" % today_data['hours'].sum())))
            st.markdown('Total Hours Worked Today')
