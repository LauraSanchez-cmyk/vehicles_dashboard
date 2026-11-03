import streamlit as st
import pandas as pd
import plotly.express as px

st.header("Análisis de anuncios de vehículos")

st.write("Explora los datos de anuncios de vehículos usados.")

car_data = pd.read_csv("vehicles_us.csv")

st.write(car_data.head())

st.header("Distribución de precios")

if st.button("Crear histograma"):
    fig = px.histogram(car_data, x="price")
    st.plotly_chart(fig)

    st.header("Relación entre precio y kilometraje")

if st.button("Crear gráfico de dispersión"):
    fig = px.scatter(car_data, x="odometer", y="price")
    st.plotly_chart(fig)