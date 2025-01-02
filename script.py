# Script principal em Python para gerenciar o pipeline de dados de leituras de temperatura de IoT
# Bibliotecas necessárias
import pandas as pd
from sqlalchemy import create_engine

# Passo 1: Ler dados do CSV
file_path = 'path_to_your_csv_file.csv'  # Substitua pelo caminho real do arquivo
data = pd.read_csv(file_path)

# Passo 2: Conectar ao PostgreSQL usando SQLAlchemy
engine = create_engine('postgresql://username:password@localhost:5432/your_database')  # Substitua pelas credenciais reais

# Passo 3: Processar e carregar dados no PostgreSQL
data.to_sql('temperature_readings', engine, if_exists='replace', index=False)

# Passo 4: Criar views SQL para análise
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

print("Dados e views criados com sucesso no PostgreSQL.")

# Passo 5: Implementação do dashboard com Streamlit
import streamlit as st
import plotly.express as px

# Título do dashboard
st.title("Dashboard de Leituras de Temperatura IoT")

# Função para buscar dados das views no PostgreSQL
def fetch_data(view_name):
    query = f"SELECT * FROM {view_name}"
    return pd.read_sql(query, engine)

# Temperatura Média por Dispositivo
st.header("Temperatura Média por Dispositivo")
avg_temp_data = fetch_data('avg_temp_por_dispositivo')
fig_avg_temp = px.bar(avg_temp_data, x='device_id', y='avg_temp', title="Temperatura Média por Dispositivo")
st.plotly_chart(fig_avg_temp)

# Leituras por Hora
st.header("Leituras por Hora")
hourly_data = fetch_data('leituras_por_hora')
fig_hourly = px.line(hourly_data, x='hora', y='contagem', title="Contagem de Leituras por Hora")
st.plotly_chart(fig_hourly)

# Temperaturas Máximas e Mínimas por Dia
st.header("Temperaturas Máximas e Mínimas por Dia")
min_max_data = fetch_data('temp_max_min_por_dia')
fig_min_max = px.line(min_max_data, x='data', y=['temp_max', 'temp_min'], title="Temperaturas Máximas e Mínimas por Dia")
st.plotly_chart(fig_min_max)

print("Dashboard Streamlit implementado com sucesso.")
