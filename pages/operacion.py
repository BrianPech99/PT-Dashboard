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

    # ===================== CRECIMIENTO HISTÓRICO POR RUTA =====================
    st.subheader("📈 Crecimiento Histórico por Ruta")
    col_ruta1, col_ruta2 = st.columns(2)

    # Lógica para Ruta 1
    with col_ruta1:
        st.markdown("<h4 style='text-align: center;'>Ruta 1</h4>", unsafe_allow_html=True)
        data_r1 = df_op[df_op['ruta'] == 'Ruta 1'].groupby("edicion")["personas_subieron"].sum().reindex(orden_ediciones).reset_index()
        fig_r1 = px.line(
            data_r1, x="edicion", y="personas_subieron", 
            markers=True, line_shape="spline",
            labels={'edicion': 'Edición', 'personas_subieron': 'Pasajeros'},
            color_discrete_sequence=["#005B96"]
        )
        st.plotly_chart(fig_r1, use_container_width=True)

    # Lógica para Ruta 2
    with col_ruta2:
        st.markdown("<h4 style='text-align: center;'>Ruta 2</h4>", unsafe_allow_html=True)
        data_r2 = df_op[df_op['ruta'] == 'Ruta 2'].groupby("edicion")["personas_subieron"].sum().reindex(orden_ediciones).reset_index()
        fig_r2 = px.line(
            data_r2, x="edicion", y="personas_subieron", 
            markers=True, line_shape="spline",
            labels={'edicion': 'Edición', 'personas_subieron': 'Pasajeros'},
            color_discrete_sequence=["#FF4DA6"] # Color distinto para diferenciar
        )
        st.plotly_chart(fig_r2, use_container_width=True)

    st.markdown("---")

    # ===================== OTROS ANÁLISIS =====================
    col_bot_left, col_bot_right = st.columns(2)

    with col_bot_left:
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

    with col_bot_right:
        # Gráfica 4: Comparativa Día de la Semana
        st.subheader("🗓️ Demanda por Día")
        # Ordenar días de la semana
        orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        # Limpieza de espacios en blanco en la columna dia_semana si existen
        df_op['dia_semana'] = df_op['dia_semana'].str.strip()
        dia_data = df_op.groupby("dia_semana")["personas_subieron"].sum().reindex(orden_dias)
        
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