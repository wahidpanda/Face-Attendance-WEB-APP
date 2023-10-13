import streamlit as st
import pandas as pd
import time
from datetime import datetime
import plotly.express as px
import os

# Function to display FizzBuzz or count
def display_fizzbuzz(count):
    if count == 0:
        st.write("Count is zero")
    elif count % 3 == 0 and count % 5 == 0:
        st.success("FizzBuzz")
    elif count % 3 == 0:
        st.success("Fizz")
    elif count % 5 == 0:
        st.success("Buzz")
    else:
        st.write(f"Count: {count}")

# Include the viewport meta tag for mobile responsiveness
st.write('<meta name="viewport" content="width=device-width, initial-scale=1">', unsafe_allow_html=True)

# Create a company banner at the top
st.image(".png", use_column_width=True) #upload your banner as png

# Display a big, bold clock
st.markdown("<h1 style='text-align: center; font-weight: bold;'>"
            f"{time.strftime('%H:%M:%S')}</h1>",
            unsafe_allow_html=True)

# Create a real-time calendar widget
selected_date = st.date_input("Select a date", datetime.now())

st.sidebar.subheader("Calendar")
st.sidebar.date_input("Select a date", selected_date)

st.sidebar.subheader("FizzBuzz Counter")
count = st.sidebar.number_input("Enter a number:", value=0, key="fizzbuzzcounter")

display_fizzbuzz(count)

st.subheader("Attendance Data")

# Define the date in the format "YYYY-MM-DD"
date = datetime.fromtimestamp(time.time()).strftime("%d-%m-%Y")

# Read the attendance data from an existing CSV file
csv_file_path = "Attendance/Attendance_" + date + ".csv"
if not os.path.exists(csv_file_path):
    st.warning(f"No attendance data found for {date}.")
else:
    # Corrected column names
    df = pd.read_csv(csv_file_path)
    df = df.rename(columns={"NAME": "Name", "TIME": "Status"})

    # Display the attendance data
    st.dataframe(df.style.highlight_max(axis=0))

    st.subheader("Data Visualization")

    # Create an interactive bar chart to visualize attendance
    fig = px.bar(df, x='Name', y='Status', color='Status',
                 labels={'Status': 'Attendance Status'},
                 title='Attendance Status for Students')
    st.plotly_chart(fig)

    # Upload CSV file and visualize data
    st.subheader("Upload Your Own CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        custom_df = pd.read_csv(uploaded_file)

        if not custom_df.empty:
            st.subheader("Uploaded Data")
            st.dataframe(custom_df)

            st.subheader("Custom Data Visualization")
            st.write("Select columns for visualization:")
            x_column = st.selectbox("X-axis column", custom_df.columns)
            y_column = st.selectbox("Y-axis column", custom_df.columns)
            y_label = st.text_input("Y-axis label", "Custom Label")

            if st.button("Visualize Data"):
                fig_custom = px.bar(custom_df, x=x_column, y=y_column,
                                    labels={y_column: y_label},
                                    title='Custom Data Visualization')
                st.plotly_chart(fig_custom)
