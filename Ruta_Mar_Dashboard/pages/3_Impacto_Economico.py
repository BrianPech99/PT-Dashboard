import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💰 Impacto Económico")

@st.cache_data
def load_data():
    return pd.read_csv("data/ruta_mar.csv")

df = load_data()

impacto_total = df["impacto_economico_total_mxn"].sum()
ahorro_promedio = df["ahorro_unitario_mxn"].mean()

col1, col2 = st.columns(2)

col1.metric("Impacto Económico Total", f"${impacto_total:,.0f}")
col2.metric("Ahorro Promedio por Usuario", f"${ahorro_promedio:,.2f}")

st.subheader("Impacto económico por ruta")

impacto_ruta = (
    df.groupby("ruta")["impacto_economico_total_mxn"]
    .sum()
    .reset_index()
)

fig = px.bar(
    impacto_ruta,
    x="ruta",
    y="impacto_economico_total_mxn",
    title="Impacto económico por ruta"
)

st.plotly_chart(fig, use_container_width=True)