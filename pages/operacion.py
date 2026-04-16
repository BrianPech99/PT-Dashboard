import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuración de la página
st.set_page_config(page_title="Operación Ruta Mar", layout="wide")

st.markdown("<h1 style='text-align: center; color:#005B96;'>🌊 Reporte de Operación - Ruta Mar</h1>", unsafe_allow_html=True)

try:
    df_op = pd.read_csv("ruta_mar.csv")
    
    # Limpieza de datos numéricos
    df_op['personas_subieron'] = pd.to_numeric(df_op['personas_subieron'], errors='coerce').fillna(0)
    df_op['impacto_economico_total_mxn'] = pd.to_numeric(df_op['impacto_economico_total_mxn'], errors='coerce').fillna(0)
    df_op['km_recorridos_por_sentido'] = pd.to_numeric(df_op['km_recorridos_por_sentido'], errors='coerce').fillna(0)

    # Orden cronológico de ediciones
    orden_ediciones = [
        "Primera Edición", "Segunda Edición", "Tercera Edición", "Cuarta Edición",
        "Quinta Edición", "Sexta Edición", "Séptima Edición", "Octava Edición",
        "Novena Edición", "Décima Edición", "Onceava Edición", "Doceava Edición"
    ]

    # ===================== KPIs =====================
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

    # ===================== FLUJO HISTÓRICO: IDA Y REGRESO =====================
    st.subheader("🔄 Flujo Histórico: Ida vs Regreso (Todas las Ediciones)")
    col_ida, col_regreso = st.columns(2)

    df_sentidos = df_op.groupby(['edicion', 'ruta', 'direccion_viaje'])['personas_subieron'].sum().reset_index()
    df_sentidos['edicion'] = pd.Categorical(df_sentidos['edicion'], categories=orden_ediciones, ordered=True)
    df_sentidos = df_sentidos.sort_values('edicion')

    with col_ida:
        st.markdown("<h4 style='text-align: center;'>⬆️ Pasajeros de IDA</h4>", unsafe_allow_html=True)
        df_ida = df_sentidos[df_sentidos['direccion_viaje'] == 'ida']
        fig_ida_gen = px.bar(df_ida, x="edicion", y="personas_subieron", color="ruta", barmode="group", text="personas_subieron",
                             color_discrete_map={"Ruta 1": "#005B96", "Ruta 2": "#FF4DA6"})
        fig_ida_gen.update_traces(textposition="outside")
        st.plotly_chart(fig_ida_gen, use_container_width=True)

    with col_regreso:
        st.markdown("<h4 style='text-align: center;'>⬇️ Pasajeros de REGRESO</h4>", unsafe_allow_html=True)
        df_reg = df_sentidos[df_sentidos['direccion_viaje'] == 'regreso']
        fig_reg_gen = px.bar(df_reg, x="edicion", y="personas_subieron", color="ruta", barmode="group", text="personas_subieron",
                             color_discrete_map={"Ruta 1": "#005B96", "Ruta 2": "#FF4DA6"})
        fig_reg_gen.update_traces(textposition="outside")
        st.plotly_chart(fig_reg_gen, use_container_width=True)

    st.markdown("---")

    # ===================== DOCEAVA EDICIÓN (NÚMEROS HORIZONTALES Y CENTRALES) =====================
    st.subheader("🚌 Detalle de Pasajeros: Doceava Edición (Ida vs Regreso)")
    df_12 = df_op[df_op['edicion'] == "Doceava Edición"]

    if not df_12.empty:
        df_12_direcciones = df_12.groupby(['ruta', 'direccion_viaje'])['personas_subieron'].sum().reset_index()
        fig_12 = px.bar(
            df_12_direcciones, x="ruta", y="personas_subieron", color="direccion_viaje",
            barmode="group", text="personas_subieron",
            color_discrete_map={"ida": "#2ECC71", "regreso": "#E74C3C"},
            labels={"personas_subieron": "Pasajeros", "direccion_viaje": "Sentido"}
        )
        
        # AJUSTE: textangle=0 para horizontal e insidetextanchor="middle" para centrar
        fig_12.update_traces(
            textposition="inside", 
            textangle=0, 
            insidetextanchor="middle",
            textfont=dict(size=20, color="white", family="Arial Black")
        )
        st.plotly_chart(fig_12, use_container_width=True)

    st.markdown("---")

    # ===================== COMPARATIVAS HISTÓRICAS =====================
    df_compare = df_op.groupby(["edicion", "ruta"])["personas_subieron"].sum().reset_index()
    df_compare["edicion"] = pd.Categorical(df_compare["edicion"], categories=orden_ediciones, ordered=True)
    df_compare = df_compare.sort_values("edicion")

    st.subheader("🚍 Comparativa de Pasajeros por Ruta (Lado a Lado)")
    fig_compare = px.bar(df_compare, x="edicion", y="personas_subieron", color="ruta", barmode="group", text="personas_subieron",
                         color_discrete_map={"Ruta 1": "#005B96", "Ruta 2": "#FF4DA6"})
    fig_compare.update_traces(textposition="outside")
    st.plotly_chart(fig_compare, use_container_width=True)

    st.subheader("📈 Crecimiento Total por Edición (Suma de Rutas)")
    df_totales_etiquetas = df_compare.groupby("edicion")["personas_subieron"].sum().reset_index()
    fig_total = px.bar(df_compare, x="edicion", y="personas_subieron", color="ruta", barmode="relative", text="personas_subieron",
                       color_discrete_map={"Ruta 1": "#005B96", "Ruta 2": "#FF4DA6"})
    fig_total.add_trace(go.Scatter(
        x=df_totales_etiquetas["edicion"], y=df_totales_etiquetas["personas_subieron"],
        text=df_totales_etiquetas["personas_subieron"], mode='text',
        textposition='top center', showlegend=False,
        textfont=dict(color='white', size=12)
    ))
    st.plotly_chart(fig_total, use_container_width=True)

    st.markdown("---")

    # ===================== TENDENCIAS [99, 901] =====================
    st.subheader("📊 Tendencia de Crecimiento por Ruta")
    col_ruta1, col_ruta2 = st.columns(2)
    valores_eje_y = list(range(100, 1000, 100)) 
    rango_visual = [99, 901] 

    with col_ruta1:
        st.markdown("<h3 style='text-align: center; color:#005B96;'>Ruta 1</h3>", unsafe_allow_html=True)
        data_r1 = df_compare[df_compare['ruta'] == 'Ruta 1']
        fig_r1 = px.line(data_r1, x="edicion", y="personas_subieron", markers=True, line_shape="spline",
                         text="personas_subieron", color_discrete_sequence=["#005B96"], range_y=rango_visual)
        fig_r1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.4)', tickvals=valores_eje_y, zeroline=False)
        fig_r1.update_traces(textposition="top center")
        st.plotly_chart(fig_r1, use_container_width=True)

    with col_ruta2:
        st.markdown("<h3 style='text-align: center; color:#FF4DA6;'>Ruta 2</h3>", unsafe_allow_html=True)
        data_r2 = df_compare[df_compare['ruta'] == 'Ruta 2']
        fig_r2 = px.line(data_r2, x="edicion", y="personas_subieron", markers=True, line_shape="spline",
                         text="personas_subieron", color_discrete_sequence=["#FF4DA6"], range_y=rango_visual)
        fig_r2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128, 128, 128, 0.4)', tickvals=valores_eje_y, zeroline=False)
        fig_r2.update_traces(textposition="top center")
        st.plotly_chart(fig_r2, use_container_width=True)

    st.markdown("---")

    # ===================== OTROS ANÁLISIS =====================
    col_bot_left, col_bot_right = st.columns(2)
    with col_bot_left:
        st.subheader("📍 Paraderos con mayor demanda")
        paraderos_data = df_op.groupby("paradero")["personas_subieron"].sum().sort_values(ascending=True).tail(12)
        fig_bar = px.bar(paraderos_data, x=paraderos_data.values, y=paraderos_data.index, orientation='h',
                         color=paraderos_data.values, color_continuous_scale='Blues')
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_bot_right:
        st.subheader("🗓️ Demanda por Día")
        orden_dias = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        df_op['dia_semana'] = df_op['dia_semana'].str.strip()
        dia_data = df_op.groupby("dia_semana")["personas_subieron"].sum().reindex(orden_dias)
        fig_dia = px.bar(dia_data, x=dia_data.index, y=dia_data.values, color=dia_data.index,
                         color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig_dia, use_container_width=True)

except Exception as e:
    st.error(f"Error al procesar los datos operativos: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Análisis de Impacto Social - Ruta Mar 2026</p>", unsafe_allow_html=True)