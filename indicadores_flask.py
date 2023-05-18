import streamlit as st
import altair as alt
import pandas as pd

# Define the data
data = pd.read_csv(r"E:\\_02_practicas_region_apurimac\\Tareas_sub gerente(David )\\Tarea_03 - indicadores\\Apurimac.csv")

g_prov = data.groupby("PROVINCIA").sum().reset_index()
g_dist = data.groupby(["PROVINCIA", "DISTRITO"]).sum().reset_index()

a_p = round(g_prov["VIVIENDAS CON LUZ"] / (g_prov["VIVIENDAS CON LUZ"] + g_prov["VIVIENDAS SIN LUZ"]) * 100, 2)
b_p = 100 - a_p

a_d = round(g_dist["VIVIENDAS CON LUZ"] / (g_dist["VIVIENDAS CON LUZ"] + g_dist["VIVIENDAS SIN LUZ"]) * 100, 2)
b_d = 100 - a_d

g_prov["% VIVIENDAS CON ACCESO"]   = a_p
g_prov["% VIVIENDAS SIN ACCESO"]   = b_p
g_dist["% VIVIENDAS CON ACCESO"] = a_d
g_dist["% VIVIENDAS SIN ACCESO"] = b_d

# Sort the data by "VIVIENDAS CON LUZ %" for province chart
g_prov = g_prov.sort_values("% VIVIENDAS CON ACCESO")

# Create the main chart using Altair
chart = (
    alt.Chart(g_prov)
    .transform_fold(
        ["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"],
        as_=["Estado de acceso", "Porcentaje"],
    )
    .mark_bar()
    .encode(
        y=alt.Y("PROVINCIA:N", sort="-x"),
        x=alt.X("Porcentaje:Q", stack="normalize", axis=alt.Axis(format=".2%")),
        color=alt.Color(
            "Estado de acceso:N",
            legend=alt.Legend(title="Estado de acceso"),
            scale=alt.Scale(
                domain=["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"],
                range=["#50B4C7", "#ED7D31"],
            ),
        ),
        order=alt.Order("Estado de acceso:N"),
    )
    .properties(
        title="BRECHAS A CUBRIR EN FLUIDO ELECTRICO POR PROVINCIA EN APURIMAC",
        width=600,
        height=400,
    )
)

# Show the main chart
st.altair_chart(chart, use_container_width=True)

# Sort the data by "VIVIENDAS CON LUZ %_d" for district chart
g_dist = g_dist.sort_values("% VIVIENDAS CON ACCESO")

# Add a subheader and display the selected province's district bar chart
selected_province = st.selectbox("Seleccione una provincia", g_prov["PROVINCIA"])
selected_province_data = g_dist[g_dist["PROVINCIA"] == selected_province]

st.subheader(f"Brecha electrica a cubrir en {selected_province}")
chart_data = pd.melt(selected_province_data, id_vars=["DISTRITO"], value_vars=["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"], var_name="Estado de acceso", value_name="Porcentaje")
chart_data["Porcentaje"] = chart_data["Porcentaje"].astype(float) / 100.0
bar_chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X("Porcentaje:Q", stack="normalize", axis=alt.Axis(format=".2%")),
    y=alt.Y("DISTRITO:N", sort="-x"),
    color=alt.Color(
        "Estado de acceso:N",
        legend=alt.Legend(title="Estado de acceso"),
        scale=alt.Scale(
            domain=["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"],
            range=["#50B4C7", "#ED7D31"],
        ),
    ),
    order=alt.Order("Estado de acceso:N")
).properties(width=600, height=400)

st.altair_chart(bar_chart, use_container_width=True)