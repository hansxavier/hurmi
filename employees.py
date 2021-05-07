import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px
from datetime import datetime

def app():
    # Read data
    checkins = pd.read_csv('ese-l1-exam-checkins-dump.csv')
    checkins['date'] = pd.to_datetime(checkins['date'], format='%Y-%m-%d')  # Convert str to DateType

    # Employee Insights
    user_list = checkins['user_id'].unique()    # User ID's

    # Fetch User ID info
    userid = st.sidebar.number_input('Enter User ID', 
                            min_value=user_list[0], 
                            max_value=user_list[-1])
    user_stats = checkins[checkins['user_id'] == userid]

    insights = st.beta_container()
    with insights:
        st.title("Employee Information")
        days, avg_work, hours, last_log = st.beta_columns(4)

        with days:
            st.title(str(user_stats['date'].nunique()))
            st.text('Total days logged in')

        with avg_work:
            avg = user_stats['hours'].sum() / user_stats['date'].nunique()
            st.title(str("%.1f" % avg))
            st.text('Average work hours per day')

        with hours:
            st.title(str(("%.1f" % user_stats['hours'].sum())))
            st.text('Total number of hours worked')
        with last_log:
            st.title(str(user_stats['date'].iloc[-1]))
            st.text('Last date logged')

        # Chart of hours worked
        choose_date, work_chart = st.beta_columns((1, 4))
        with choose_date:
            st.markdown("**Daily Check-In Hours**")
            # Set min and max dates available in dataset
            sort_dates = user_stats
            start_date = st.date_input('Start Date', 
                                        value = sort_dates['date'].min(),
                                        min_value = sort_dates['date'].min(),
                                        max_value = sort_dates['date'].max())
            end_date = st.date_input('End Date', 
                                        value = sort_dates['date'].max(),
                                        min_value = sort_dates['date'].min(),
                                        max_value = sort_dates['date'].max())
            
            start_date = pd.to_datetime(start_date, format='%Y-%m-%d')
            end_date   = pd.to_datetime(end_date, format='%Y-%m-%d')
        with work_chart:
            if start_date <= end_date:
                # Group each day with the # of hours worked
                date_hours = sort_dates.groupby(['date'])['hours'].agg('sum').reset_index()

                # Filter graph between start and end date
                date_hours = date_hours.loc[(date_hours['date'] >= start_date) & (date_hours['date'] <= end_date)]
                date_hours = date_hours.rename(columns={'date':'Date'}).reset_index()
                fig_date_hours = px.bar(date_hours, x='Date', y='hours')
                st.plotly_chart(fig_date_hours, use_container_width=True)

            else:
                st.error('Error: End date must fall after start date.')


    # Project-Specific Insights
    st.title("Project-Specific Statistics")
    projects = st.beta_expander("Expand")
    with projects:
        project_hour_breakdown, project_insights = st.beta_columns((4, 1))
        with project_hour_breakdown:
            st.title("Daily Project Breakdown")
            breakdown = user_stats.groupby(['date', 'project_id'])['hours'].sum().reset_index()
            breakdown = breakdown.pivot(index='date', columns='project_id', values='hours').fillna(0).reset_index()
            fig_breakdown = px.bar(breakdown, x="date", y=breakdown.columns[1:])
            st.plotly_chart(fig_breakdown, use_container_width=True)

        with project_insights:
            st.title(str(user_stats['project_id'].nunique()))
            st.markdown('Unique projects user has contributed')

        most_active_projects, charts = st.beta_columns((1,2))
        with most_active_projects:
            st.title("Most Active Projects")
            most_active = user_stats.groupby('project_id')['hours'].sum().reset_index().sort_values(by=['hours'])
            most_active['project_id'] = most_active['project_id'].astype(str)

            # Displays 5 most active projects of user 
            fig_most_active = px.pie(most_active[-5:], values='hours', names='project_id')
            st.plotly_chart(fig_most_active, use_container_width=True)

        with charts:
            st.title("Hours Worked per Project")
            # Groups each Project by the number of hours worked on it
            project_hours = user_stats.groupby('project_id')['hours'].sum().reset_index() # .rename(columns={'project_id':'Project ID'}).set_index('Project ID')
            project_hours['project_id'] = project_hours['project_id'].astype(str)
            fig_project_hours = px.bar(project_hours, x='project_id', y='hours')
            st.plotly_chart(fig_project_hours, use_container_width=True)
