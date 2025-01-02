# Main Python script to handle the data pipeline for IoT temperature readings
# Libraries needed
import pandas as pd
from sqlalchemy import create_engine

# Step 1: Read CSV data
file_path = 'path_to_your_csv_file.csv'  # Replace with actual file path
data = pd.read_csv(file_path)

# Step 2: Connect to PostgreSQL using SQLAlchemy
engine = create_engine('postgresql://username:password@localhost:5432/your_database')  # Replace with actual credentials

# Step 3: Process and load data into PostgreSQL
data.to_sql('temperature_readings', engine, if_exists='replace', index=False)

# Step 4: Create SQL views for analysis
with engine.connect() as conn:
    conn.execute('''
    CREATE OR REPLACE VIEW avg_temp_por_dispositivo AS
    SELECT device_id, AVG(temperature) as avg_temp
    FROM temperature_readings
    GROUP BY device_id;
    ''')
    
    conn.execute('''
    CREATE OR REPLACE VIEW leituras_por_hora AS
    SELECT EXTRACT(HOUR FROM timestamp) as hora, COUNT(*) as contagem
    FROM temperature_readings
    GROUP BY hora;
    ''')
    
    conn.execute('''
    CREATE OR REPLACE VIEW temp_max_min_por_dia AS
    SELECT DATE(timestamp) as data, MAX(temperature) as temp_max, MIN(temperature) as temp_min
    FROM temperature_readings
    GROUP BY data;
    ''')

print("Data and views have been successfully created in PostgreSQL.")

# Step 5: Dashboard Implementation with Streamlit
import streamlit as st
import plotly.express as px

# Dashboard title
st.title("IoT Temperature Readings Dashboard")

# Function to fetch data from PostgreSQL views
def fetch_data(view_name):
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql(query, engine)

# Average Temperature by Device
st.header("Average Temperature by Device")
avg_temp_data = fetch_data('avg_temp_por_dispositivo')
fig_avg_temp = px.bar(avg_temp_data, x='device_id', y='avg_temp', title="Average Temperature by Device")
st.plotly_chart(fig_avg_temp)

# Readings by Hour
st.header("Readings by Hour")
hourly_data = fetch_data('leituras_por_hora')
fig_hourly = px.line(hourly_data, x='hora', y='contagem', title="Readings Count by Hour")
st.plotly_chart(fig_hourly)

# Max and Min Temperatures by Day
st.header("Max and Min Temperatures by Day")
min_max_data = fetch_data('temp_max_min_por_dia')
fig_min_max = px.line(min_max_data, x='data', y=['temp_max', 'temp_min'], title="Max and Min Temperatures by Day")
st.plotly_chart(fig_min_max)

print("Streamlit dashboard implemented successfully.")
