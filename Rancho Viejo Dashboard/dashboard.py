import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Ruta Mar - Planeación Ruta 3 Rancho Viejo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Encabezado
st.markdown(
    "<h1 style='text-align: center; color:#FF4DA6;'>🌴 Ruta Mar - Planeación Ruta 3 Rancho Viejo</h1>",
    unsafe_allow_html=True
)

# Cargar datos (Asegúrate de que el CSV esté en la raíz de tu repo de GitHub)
try:
    df = pd.read_csv("Rancho_Viejo_RutaMar.csv")
except FileNotFoundError:
    st.error("No se encontró el archivo 'Rancho_Viejo_RutaMar.csv'. Verifica que esté en la raíz del repositorio.")
    st.stop()

# ===================== DEFINICIÓN DE ORDEN CRONOLÓGICO =====================
# Listas maestras para que las gráficas sigan el orden del reloj y no el alfabético
orden_ida = [
    "09:00 am", "10:00 am", "11:00 am", "12:00 pm", "13:00 pm", 
    "14:00 pm", "15:00 pm", "16:00 pm", "17:00 pm", "18:00 pm", "19:00 pm"
]

orden_regreso = [
    "08:00 am", "09:00 am", "10:00 am", "11:00 am", "12:00 pm", "13:00 pm", 
    "14:00 pm", "15:00 pm", "16:00 pm", "17:00 pm", "18:00 pm", "19:00 pm", "20:00 pm"
]

# ===================== KPIs =====================
col1, col2, col3, col4 = st.columns(4)

# Aceptación
aceptacion = (df["¿Usarías un transporte gratuito para ir a la playa los fines de semana?"] == "Si").mean() * 100
col1.metric("Aceptación del programa", f"{aceptacion:.1f}%")

# Paraderos
paraderos = df["¿En dónde les gustaría tomar el camión para ir a la playa?\nSelecciona solamente 4"].dropna().str.split(";").explode().nunique()
col2.metric("Paraderos solicitados", paraderos)

# Horarios Pico (procesamiento de datos para métricas)
horarios_ida = df["IDA\n¿En que horario te gustaría que pase la ruta?\nSelecciona 4"].dropna().str.split(";").explode()
horario_ida_top = horarios_ida.value_counts().idxmax()
col3.metric("Horario pico de ida", horario_ida_top)

horarios_regreso = df["REGRESO\n¿En que horario te gustaría que pase la ruta?\nSelecciona 4"].dropna().str.split(";").explode()
horario_regreso_top = horarios_regreso.value_counts().idxmax()
col4.metric("Horario pico de regreso", horario_regreso_top)

st.markdown("---")

# ===================== DEMANDA POTENCIAL =====================
st.subheader("📊 Demanda Potencial")
frecuencia = df["¿Con que frecuencia vas a la playa?"].value_counts()
fig_frecuencia = px.bar(
    frecuencia,
    x=frecuencia.index,
    y=frecuencia.values,
    color=frecuencia.index,
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_frecuencia, use_container_width=True)

# ===================== PARADEROS =====================
st.subheader("🚌 Paraderos más solicitados")
paraderos_exp = df["¿En dónde les gustaría tomar el camión para ir a la playa?\nSelecciona solamente 4"].dropna().str.split(";").explode()
top_paraderos = paraderos_exp.value_counts().head(10)
fig_paraderos = px.bar(
    top_paraderos,
    x=top_paraderos.index,
    y=top_paraderos.values,
    color=top_paraderos.index,
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_paraderos, use_container_width=True)

# ===================== HORARIOS (ORDENADOS) =====================
st.subheader("⏰ Horarios preferidos")

# Histograma de Ida con orden cronológico
fig_ida = px.histogram(
    horarios_ida,
    x=horarios_ida,
    color=horarios_ida,
    color_discrete_sequence=px.colors.qualitative.Set3,
    category_orders={"x": orden_ida} # <--- Orden cronológico aplicado
)
fig_ida.update_layout(xaxis_title="Hora de Salida", yaxis_title="Cantidad de Personas")

# Histograma de Regreso con orden cronológico
fig_regreso = px.histogram(
    horarios_regreso,
    x=horarios_regreso,
    color=horarios_regreso,
    color_discrete_sequence=px.colors.qualitative.Set3,
    category_orders={"x": orden_regreso} # <--- Orden cronológico aplicado
)
fig_regreso.update_layout(xaxis_title="Hora de Regreso", yaxis_title="Cantidad de Personas")

col5, col6 = st.columns(2)
with col5:
    st.markdown("**Horarios de ida**")
    st.plotly_chart(fig_ida, use_container_width=True)
with col6:
    st.markdown("**Horarios de regreso**")
    st.plotly_chart(fig_regreso, use_container_width=True)

# ===================== ACEPTACIÓN =====================
st.subheader("✅ Aceptación del programa")
aceptacion_counts = df["¿Usarías un transporte gratuito para ir a la playa los fines de semana?"].value_counts()
fig_aceptacion = px.pie(
    aceptacion_counts,
    names=aceptacion_counts.index,
    values=aceptacion_counts.values,
    color=aceptacion_counts.index,
    color_discrete_sequence=px.colors.qualitative.Set3
)
st.plotly_chart(fig_aceptacion, use_container_width=True)

st.markdown("---")
st.markdown(
    "<h3 style='text-align: center; color:#005B96;'>Dashboard de Planeación - Ruta 3 Rancho Viejo</h3>",
    unsafe_allow_html=True
)