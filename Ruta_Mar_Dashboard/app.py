import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Ruta Mar",
    layout="wide"
)

st.title("🚍 Dashboard Ruta Mar")
st.markdown("Análisis del servicio de transporte gratuito hacia playas")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("data/ruta_mar.csv")
    return df

df = load_data()

st.subheader("Vista previa del dataset")
st.dataframe(df.head())

# KPIs principales
total_pasajeros = df["personas_subieron"].sum()
impacto_total = df["impacto_economico_total_mxn"].sum()
total_viajes = df["unidad"].nunique()
km_totales = df["km_recorridos_por_sentido"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Pasajeros", f"{total_pasajeros:,}")
col2.metric("Impacto Económico", f"${impacto_total:,.0f}")
col3.metric("Unidades", total_viajes)
col4.metric("Km recorridos", f"{km_totales:,.0f}")

st.info("Usa el menú lateral para explorar los análisis.")