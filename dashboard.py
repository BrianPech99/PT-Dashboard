import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(
    page_title="Planeación Ruta 3 - Rancho Viejo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título centrado fijo
st.markdown("<h1 style='text-align: center; color:#FF4DA6;'>🌴 Ruta 3 - Planeación Rancho Viejo</h1>", unsafe_allow_html=True)

# 2. Cargar datos (Solo el de la encuesta)
try:
    df = pd.read_csv("Rancho_Viejo_RutaMar.csv")
    
    # Renombrar columnas para estabilidad
    df.columns = [
        "timestamp", 
        "frecuencia", 
        "paraderos", 
        "horario_ida", 
        "horario_regreso", 
        "aceptacion"
    ]
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.stop()

# 3. Listas de Orden Cronológico
orden_ida = ["09:00 am", "10:00 am", "11:00 am", "12:00 pm", "13:00 pm", "14:00 pm", "15:00 pm", "16:00 pm", "17:00 pm", "18:00 pm", "19:00 pm"]
orden_regreso = ["08:00 am", "09:00 am", "10:00 am", "11:00 am", "12:00 pm", "13:00 pm", "14:00 pm", "15:00 pm", "16:00 pm", "17:00 pm", "18:00 pm", "19:00 pm", "20:00 pm"]

# ===================== KPIs =====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    aceptacion_val = (df["aceptacion"] == "Si").mean() * 100
    st.metric("Aceptación del programa", f"{aceptacion_val:.1f}%")

with col2:
    paraderos_exp = df["paraderos"].dropna().str.split(";").explode()
    st.metric("Paraderos solicitados", paraderos_exp.nunique())

with col3:
    ida_exp = df["horario_ida"].dropna().str.split(";").explode()
    st.metric("Horario pico ida", ida_exp.value_counts().idxmax())

with col4:
    regreso_exp = df["horario_regreso"].dropna().str.split(";").explode()
    st.metric("Horario pico regreso", regreso_exp.value_counts().idxmax())

st.markdown("---")

# ===================== DEMANDA POTENCIAL =====================
st.subheader("📊 Demanda Potencial")
frecuencia_data = df["frecuencia"].value_counts()
fig_frec = px.bar(
    frecuencia_data, 
    x=frecuencia_data.index, 
    y=frecuencia_data.values, 
    color=frecuencia_data.index, 
    color_discrete_sequence=px.colors.qualitative.Set3,
    labels={'x': 'Frecuencia de visita', 'y': 'Número de personas'}
)
st.plotly_chart(fig_frec, use_container_width=True)

# ===================== PARADEROS =====================
st.subheader("🚌 Paraderos más solicitados")
top_paraderos = paraderos_exp.value_counts().head(10)
fig_paraderos = px.bar(
    top_paraderos,
    x=top_paraderos.index,
    y=top_paraderos.values,
    color=top_paraderos.index,
    color_discrete_sequence=px.colors.qualitative.Set3,
    labels={'x': 'Ubicación del paradero', 'y': 'Menciones/Votos'}
)
st.plotly_chart(fig_paraderos, use_container_width=True)

# ===================== HORARIOS (ORDENADOS) =====================
st.subheader("⏰ Horarios preferidos")

# Convertir a Categorical para asegurar orden cronológico
ida_exp_cat = pd.Categorical(ida_exp, categories=orden_ida, ordered=True)
regreso_exp_cat = pd.Categorical(regreso_exp, categories=orden_regreso, ordered=True)

col5, col6 = st.columns(2)

with col5:
    st.markdown("**Horarios de ida**")
    fig_i = px.histogram(
        x=ida_exp_cat, 
        color=ida_exp_cat, 
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={'x': 'Hora de salida', 'y': 'Demanda (Votos)'}
    )
    fig_i.update_xaxes(categoryorder='array', categoryarray=orden_ida)
    st.plotly_chart(fig_i, use_container_width=True)

with col6:
    st.markdown("**Horarios de regreso**")
    fig_r = px.histogram(
        x=regreso_exp_cat, 
        color=regreso_exp_cat, 
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={'x': 'Hora de retorno', 'y': 'Demanda (Votos)'}
    )
    fig_r.update_xaxes(categoryorder='array', categoryarray=orden_regreso)
    st.plotly_chart(fig_r, use_container_width=True)

# ===================== ACEPTACIÓN =====================
st.subheader("✅ Aceptación del programa")
aceptacion_counts = df["aceptacion"].value_counts()
fig_pie = px.pie(
    aceptacion_counts, 
    names=aceptacion_counts.index, 
    values=aceptacion_counts.values, 
    color_discrete_sequence=px.colors.qualitative.Set3
)
fig_pie.update_traces(textinfo='percent+label')
st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.markdown("<h3 style='text-align: center; color:#005B96;'>Ruta 3 - Planeación Rancho Viejo</h3>", unsafe_allow_html=True)
