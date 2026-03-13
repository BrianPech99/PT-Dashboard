import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⏱ Operación y Puntualidad")

@st.cache_data
def load_data():
    return pd.read_csv("data/ruta_mar.csv")

df = load_data()

df["hora_programada"] = pd.to_datetime(df["hora_programada"], errors="coerce")
df["hora_real"] = pd.to_datetime(df["hora_real"], errors="coerce")

df["retraso_min"] = (df["hora_real"] - df["hora_programada"]).dt.total_seconds() / 60

st.subheader("Retraso promedio por ruta")

retraso_ruta = df.groupby("ruta")["retraso_min"].mean().reset_index()

fig = px.bar(
    retraso_ruta,
    x="ruta",
    y="retraso_min",
    title="Retraso promedio por ruta (min)"
)

st.plotly_chart(fig, use_container_width=True)