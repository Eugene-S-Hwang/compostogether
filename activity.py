import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Function to load data from Google Sheets

def load_data():
    # Define the scope
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

    # Add credentials
    creds = ServiceAccountCredentials.from_json_keyfile_name('compostogether-data-c8dd8dad8d01.json', scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet
    sheet = client.open("activity").sheet1

    # Get all records
    data = sheet.get_all_records()
    result = pd.DataFrame(data)
    result.sort_values(by=["Date"], inplace=True, ignore_index=True)
    return result
    # data =  pd.read_csv("Testing_Activity.csv")
    # return data

# Load data
st.title("History of Activity of Compost Bins")
# st.write("Displaying data from Google Sheets")

data = load_data()

# Display data
# st.write(data)

# Plotly chart
if not data.empty:
    fig = px.line(data, x='Date', y='Check Temperature', title='History of Temperature')
    st.plotly_chart(fig)
else:
    st.write("No data available")

if not data.empty:
    green_data = data[["Date", "Greens"]]
    prev = 0
    # st.write(green_data)
    for i in range(len(green_data["Greens"])):
        # st.write(green_data["Greens"][i])
        green_data["Greens"][i] = float(green_data["Greens"][i]) + prev
        prev = green_data["Greens"][i]
        # st.write(green_data["Greens"][i])
        # st.write("______________")
    fig = px.line(green_data, x='Date', y='Greens', title="History of Amount of Greens")
    st.plotly_chart(fig)
else:
    st.write("No graph available")

if not data.empty:
    brown_data = data[["Date", "Browns"]]
    prev = 0
    # st.write(green_data)
    for i in range(len(brown_data["Browns"])):
        # st.write(green_data["Greens"][i])
        brown_data["Browns"][i] = float(brown_data["Browns"][i]) + prev
        prev = brown_data["Browns"][i]
        # st.write(green_data["Greens"][i])
        # st.write("______________")
    fig = px.line(brown_data, x='Date', y='Browns', title="History of Amount of Browns")
    st.plotly_chart(fig)
else:
    st.write("No graph available")