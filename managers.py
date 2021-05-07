import streamlit as st
import pandas as pd
import numpy as np 
import plotly.express as px
from datetime import datetime

def app():
    # Read data
    checkins = pd.read_csv('ese-l1-exam-checkins-dump.csv')
    checkins['date'] = pd.to_datetime(checkins['date'], format='%Y-%m-%d')  # Convert str to DateType

    # Manager Insights
    manager_list = checkins['manager_id'].unique()

    # Fetch Manager Info
    managerid = st.sidebar.number_input('Enter Manager ID', 
                                        min_value=manager_list.min(), 
                                        max_value=manager_list.max())
    man_stats = checkins[checkins['manager_id'] == managerid]
    
    insights = st.beta_container()
    with insights:
        st.title("Manager Information")

        unq_projects, no_of_emps, proj_hrs = st.beta_columns(3)
        with unq_projects:
            st.title(man_stats['project_id'].nunique())
            st.text('Number of Projects Handled')
        with no_of_emps:
            st.title(man_stats['user_id'].nunique())
            st.text('Number of Employees')
        with proj_hrs:
            st.title(man_stats['hours'].sum())
            st.text('Cumulative Project Hours')

    project_workload = st.beta_container()
    with project_workload:
        st.title("Project Workload Distribution")
        # Workload Distribution of each Employee per Project
        dist = man_stats.groupby(['project_id', 'user_id'])['hours'].sum().reset_index()
        dist = dist.sort_values('hours')
        dist['project_id'] = dist['project_id'].astype(str)
        dist = dist.pivot(index='project_id', columns='user_id', values='hours').fillna(0).reset_index()
        fig_dist = px.bar(dist, x='project_id', y=dist.columns[0:])
        st.plotly_chart(fig_dist, use_container_width=True)

    # pid_list = checkins['project_id'].unique()
    # man_plist = man_stats['project_id'].unique()
    # # Specific Project Insights
    # pid_choose, proj_graph = st.beta_columns((1, 3))
    # with pid_choose:
    #     pid = st.number_input('Enter Project ID', 
    #                             min_value=pid_list.min(), 
    #                             max_value=pid_list.max())
    # with proj_graph:
    #     if pid in man_plist:
    #         proj_filter = man_stats.loc[man_stats['project_id'] == pid]
    #         proj_filter = proj_filter.groupby(['project_id', 'user_id'])['hours'].sum().reset_index()
    #         proj_filter = proj_filter.pivot(index='project_id', columns='user_id', values='hours').fillna(0).reset_index()
    #         fig_proj = px.bar(proj_filter, x='project_id', y=dist.columns[0:])
    #         st.plotly_chart(fig_proj, use_container_width=True)

    #     else:
    #         st.error('Error: Current Manager does not handle Project.')




app()