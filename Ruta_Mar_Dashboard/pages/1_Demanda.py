import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Demanda del Transporte")

@st.cache_data
def load_data():
    return pd.read_csv("data/ruta_mar.csv")

df = load_data()

st.subheader("Pasajeros por Ruta")

df_ruta = df.groupby("ruta")["personas_subieron"].sum().reset_index()

fig = px.bar(
    df_ruta,
    x="ruta",
    y="personas_subieron",
    title="Pasajeros por ruta"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Paraderos")

top_paraderos = (
    df.groupby("paradero")["personas_subieron"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig2 = px.bar(
    top_paraderos,
    x="paradero",
    y="personas_subieron",
    title="Top 10 paraderos con más usuarios"
)

st.plotly_chart(fig2, use_container_width=True)