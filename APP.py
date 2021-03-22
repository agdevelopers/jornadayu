#Importing Packets
from numpy.lib.function_base import kaiser
import streamlit as st
import pandas as pd
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import pydeck as pdk

#Reading Spreadshhet
df=pd.read_csv('./dataset.csv')
df.insert(loc=7, column='status_job', value='Período Integral')
df.insert(loc=8, column='expirience', value='02 anos')

cities = df.city.drop_duplicates()
cities = cities.sort_values()
jobs = df.job_title.drop_duplicates()
jobs = jobs.sort_values()

try:
    #Dashboard
    st.title('Jornada YU')
    st.sidebar.image('./logo.png')
    st.sidebar.subheader('Pesquisa de Salários')

    st.sidebar.header('Cargo')
    cargo = st.sidebar.selectbox('Selecione o Cargo:', (jobs))

    st.sidebar.header('Tempo de Experiência')
    tempo = st.sidebar.selectbox('Selecione o tempo:', (df.expirience))

    st.sidebar.header('Cidade')
    cidade = st.sidebar.selectbox('Selecione a Cidade:', (cities))

    st.sidebar.header('Status da Vaga')
    status = st.sidebar.selectbox('Selecione o Status:', (df.status_job))

    dataset = df.loc[(df['city'] == cidade) & (df['job_title'] == cargo)]
    minimo = int(round(dataset.average_current_salary.min()))
    media = int(round(dataset.average_current_salary.mean()))
    mediana = int(round(dataset.average_current_salary.median()))
    moda = int(round(dataset.average_current_salary.mode()))
    maximo = int(round(dataset.average_current_salary.max()))
    dados = pd.DataFrame({'Mínimo':[minimo], 'Moda':[moda], 'Média':[media], 'Mediana':[mediana], 'Máximo':[maximo]})

    publico = dataset.initials.value_counts().sum()
    st.subheader('Estimativa da YU vagas.')
    st.write(f'*Foram entrevistados **{publico}** profissionais para esta pesquisa.')

    #Gráfico
    fig = go.Figure(data=[go.Bar(name='Mínimo', orientation='v',  textposition='auto', opacity=0.9, marker=dict(color='rgb(25,25,112)'), text=dados.Mínimo, y=dados.Mínimo, x=dados.index),
                        go.Bar(name='Mais Frequente', orientation='v',  textposition='auto', opacity=0.9, marker=dict(color='rgb(0,191,255)'), text=dados.Moda, y=dados.Moda, x=dados.index),
                        go.Bar(name='Média', orientation='v',  textposition='auto', opacity=0.9, marker=dict(color='rgb(99,110,250)'), text=dados.Média, y=dados.Média, x=dados.index),
                        go.Bar(name='Salario Central', orientation='v',  textposition='auto', opacity=0.9, marker=dict(color='rgb(0,204,150)'), text=dados.Mediana, y=dados.Mediana, x=dados.index),
                        go.Bar(name='Máximo', orientation='v',  textposition='auto', opacity=0.9, marker=dict(color='rgb(171,99,250)'), text=dados.Máximo, y=dados.Máximo, x=dados.index)])
    fig.update_layout(barmode='group', title_text= 'Faixa Salarial')
    fig
    #Mapa
    st.subheader('Mapa das Vagas')
    st.pydeck_chart(pdk.Deck(initial_view_state=pdk.ViewState(latitude=-23.6149576,longitude=-46.6204729,zoom=8,pitch=50),
    layers=[pdk.Layer('HexagonLayer',
    data=dataset[['latitude','longitude']],
    get_position='[longitude, latitude]',
    auto_highlight=True,
    elevation_scale=50,
    pickable=True,
    elevation_range=[0,3000],
    extruded=True,
    coverage=1)]))

except:
    st.write(f'OPS! Infelizmente não há dados para esta pesquisa. Para retornar aperte F5 no seu teclado.')
