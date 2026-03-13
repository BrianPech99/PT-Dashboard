import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuración de la página
st.set_page_config(page_title="Operación Ruta Mar", layout="wide")

st.markdown("<h1 style='text-align: center; color:#005B96;'>🌊 Reporte de Operación - Ruta Mar</h1>", unsafe_allow_html=True)

try:
    df_op = pd.read_csv("ruta_mar.csv")
    
    # Limpieza: Asegurar que las columnas numéricas sean tratadas como tal
    df_op['personas_subieron'] = pd.to_numeric(df_op['personas_subieron'], errors='coerce').fillna(0)
    df_op['impacto_economico_total_mxn'] = pd.to_numeric(df_op['impacto_economico_total_mxn'], errors='coerce').fillna(0)

    # 2. Definir orden cronológico de las Ediciones
    orden_ediciones = [
        "Primera Edición", "Segunda Edición", "Tercera Edición", "Cuarta Edición",
        "Quinta Edición", "Sexta Edición", "Séptima Edición", "Octava Edición",
        "Novena Edición", "Décima Edición", "Onceava Edición", "Doceava Edición"
    ]

    # ===================== KPIs PRINCIPALES =====================
    c1, c2, c3, c4 = st.columns(4)
    
    total_pasajeros = df_op["personas_subieron"].sum()
    ahorro_total = df_op["impacto_economico_total_mxn"].sum()
    km_totales = df_op["km_recorridos_por_sentido"].sum()
    promedio_por_viaje = df_op.groupby(['fecha_operacion', 'ruta', 'unidad', 'direccion_viaje'])['personas_subieron'].sum().mean()

    c1.metric("Total Pasajeros", f"{total_pasajeros:,.0f}")
    c2.metric("Ahorro Comunitario", f"${ahorro_total:,.2f} MXN")
    c3.metric("Distancia Total", f"{km_totales:,.1f} km")
    c4.metric("Promedio Pasajeros/Viaje", f"{promedio_por_viaje:.1f}")

    st.markdown("---")

    # ===================== GRÁFICAS DE OPERACIÓN =====================
    col_left, col_right = st.columns(2)

    with col_left:
        # Gráfica 1: Crecimiento por Edición
        st.subheader("📈 Crecimiento Histórico")
        edicion_data = df_op.groupby("edicion")["personas_subieron"].sum().reindex(orden_ediciones).reset_index()
        fig_line = px.line(
            edicion_data, x="edicion", y="personas_subieron", 
            markers=True, line_shape="spline",
            labels={'edicion': 'Edición del Programa', 'personas_subieron': 'Pasajeros'},
            color_discrete_sequence=["#005B96"]
        )
        st.plotly_chart(fig_line, use_container_width=True)

        # Gráfica 2: Distribución por Ruta
        st.subheader("🚌 Uso por Ruta")
        ruta_data = df_op.groupby("ruta")["personas_subieron"].sum()
        fig_pie = px.pie(
            values=ruta_data.values, names=ruta_data.index,
            hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        # Gráfica 3: Top Paraderos con más subidas
        st.subheader("📍 Paraderos con mayor demanda (Subidas)")
        paraderos_data = df_op.groupby("paradero")["personas_subieron"].sum().sort_values(ascending=True).tail(12)
        fig_bar = px.bar(
            paraderos_data, x=paraderos_data.values, y=paraderos_data.index,
            orientation='h', color=paraderos_data.values,
            color_continuous_scale='Blues',
            labels={'x': 'Total de personas', 'y': ''}
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Gráfica 4: Comparativa Día de la Semana
        st.subheader("🗓️ Demanda por Día")
        dia_data = df_op.groupby("dia_semana")["personas_subieron"].sum()
        fig_dia = px.bar(
            dia_data, x=dia_data.index, y=dia_data.values,
            color=dia_data.index, color_discrete_sequence=px.colors.qualitative.Set2,
            labels={'dia_semana': 'Día', 'y': 'Pasajeros'}
        )
        st.plotly_chart(fig_dia, use_container_width=True)

except Exception as e:
    st.error(f"Error al procesar los datos operativos: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Análisis de Impacto Social - Ruta Mar 2026</p>", unsafe_allow_html=True)