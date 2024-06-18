import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta
from st_aggrid import AgGrid, GridOptionsBuilder

def create_db_connection():
    conn = sqlite3.connect('events.db')
    return conn

def fetch_events_from_db(conn):
    query = "SELECT * FROM events"
    return pd.read_sql_query(query, conn)

def generate_calendar_view(start_date, end_date):
    date_range = pd.date_range(start=start_date, end=end_date)
    calendar = pd.DataFrame(date_range, columns=['Date'])
    calendar['Day'] = calendar['Date'].dt.day_name()
    return calendar

def add_events_to_calendar(calendar, events):
    calendar['Events'] = ''
    for idx, row in calendar.iterrows():
        day_events = events[(events['start'] <= row['Date'].isoformat()) & (events['end'] >= row['Date'].isoformat())]
        if not day_events.empty:
            calendar.at[idx, 'Events'] = ', '.join(day_events['summary'])
    return calendar

# Streamlit app
st.title("SQLite Calendar Events")

# Connect to SQLite database and fetch events
conn = create_db_connection()
events_df = fetch_events_from_db(conn)

# Convert start and end columns to datetime
events_df['start'] = pd.to_datetime(events_df['start'])
events_df['end'] = pd.to_datetime(events_df['end'])

# Generate calendar view for the next 30 days
start_date = datetime.now()
end_date = start_date + timedelta(days=30)
calendar_df = generate_calendar_view(start_date, end_date)

# Add events to calendar view
calendar_with_events = add_events_to_calendar(calendar_df, events_df)

# Display calendar
st.write("Upcoming events in calendar view:")
gb = GridOptionsBuilder.from_dataframe(calendar_with_events)
gb.configure_pagination()
gb.configure_columns(["Date", "Day", "Events"], editable=False)
grid_options = gb.build()
AgGrid(calendar_with_events, gridOptions=grid_options)

conn.close()
