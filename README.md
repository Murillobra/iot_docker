# iot_docker

Pipeline de Dados IoT com Docker e Streamlit

Visão Geral

Este projeto implementa um pipeline de dados para processar leituras de temperatura de dispositivos IoT, armazená-las em um banco de dados PostgreSQL e visualizá-las usando um dashboard Streamlit. Todo o sistema utiliza Docker para containerização e Python para processamento de dados.

Funcionalidades

Ingestão de Dados: Processa leituras de temperatura de dispositivos IoT a partir de um arquivo CSV.

Integração com Banco de Dados: Armazena dados em um banco PostgreSQL e cria views SQL para análise.

Visualização: Exibe insights usando gráficos interativos em um dashboard Streamlit.

Pré-requisitos

Git

Instale o Git e configure-o com seu nome de usuário e email.

git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"

Docker

Instale o Docker e garanta que ele esteja em execução.

Crie um container PostgreSQL:

docker run --name postgres-iot -e POSTGRES_PASSWORD=sua_senha -p 5432:5432 -d postgres

Python

Instale o Python (3.8 ou mais recente).

Crie um ambiente virtual e instale as bibliotecas necessárias:

pip install pandas psycopg2-binary sqlalchemy streamlit plotly

Instalação

Clone o repositório:

git clone <repository_url>
cd <repository_name>

Adicione o arquivo CSV com as leituras de temperatura IoT ao diretório do projeto e atualize o file_path no script.

Uso

Execute o script do pipeline de dados para ingerir dados e criar views SQL:

python pipeline.py

Inicie o dashboard Streamlit:

streamlit run dashboard.py

Acesse o dashboard no navegador em http://localhost:8501.

Views SQL Explicadas

avg_temp_por_dispositivo:

Exibe a temperatura média por dispositivo IoT.

Exemplo:

SELECT device_id, AVG(temperature) as avg_temp
FROM temperature_readings
GROUP BY device_id;

leituras_por_hora:

Conta o número de leituras de temperatura para cada hora do dia.

SELECT EXTRACT(HOUR FROM timestamp) as hora, COUNT(*) as contagem
FROM temperature_readings
GROUP BY hora;

temp_max_min_por_dia:

Mostra as temperaturas máxima e mínima registradas por dia.

SELECT DATE(timestamp) as data, MAX(temperature) as temp_max, MIN(temperature) as temp_min
FROM temperature_readings
GROUP BY data;

Exemplos de Saídas

Gráfico de Barras: Temperatura média por dispositivo.

Gráfico de Linhas: Contagem de leituras por hora.

Gráfico de Linhas: Temperaturas máxima e mínima por dia.

Contribuição

Faça um fork do repositório.

Crie uma branch para sua funcionalidade.

Envie um pull request com uma explicação detalhada.

