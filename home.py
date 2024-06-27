import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Function to load data from Google Sheets
def load_data():
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Add credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name('compostogether-data-c8dd8dad8d01.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open("Composting Weekly Log").sheet1

    # Get all records
    data = sheet.get_all_records()
    return pd.DataFrame(data)
    # data =  pd.read_csv("Testing_Activity.csv")
    # return data

# Load data
st.title("Community Composting Program Weekly Log")
st.write("Displaying data from Google Sheets")

data = load_data()

# Display data
st.write(data)

# Plotly chart
if not data.empty:
    fig = px.line(data, x='Date', y='Check Temperature', title='Weekly Composting Data')
    st.plotly_chart(fig)
else:
    st.write("No data available")

