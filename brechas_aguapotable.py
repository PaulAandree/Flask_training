import streamlit as st
import altair as alt
import pandas as pd
import altair_saver

# Define the data
data = pd.read_csv(r"E:\\_02_practicas_region_apurimac\\Tareas_sub gerente(David )\\Tarea_07_brechas de Saneamiento\\Apurimac_aguapotable.csv")

g_prov_agua = data.groupby("PROVINCIA").sum().reset_index()
g_dist_agua = data.groupby(["PROVINCIA", "DISTRITO"]).sum().reset_index()

p_con_agua = round(g_prov_agua["VIVIENDAS CON AGUA"] / (g_prov_agua["VIVIENDAS CON AGUA"] + g_prov_agua["VIVIENDAS SIN AGUA"]) * 100, 2)
p_sin_agua = 100 - p_con_agua

d_con_agua = round(g_dist_agua["VIVIENDAS CON AGUA"] / (g_dist_agua["VIVIENDAS CON AGUA"] + g_dist_agua["VIVIENDAS SIN AGUA"]) * 100, 2)
d_sin_agua = 100 - d_con_agua

g_prov_agua["% VIVIENDAS CON ACCESO"]   = p_con_agua
g_prov_agua["% VIVIENDAS SIN ACCESO"]   = p_sin_agua
g_dist_agua["% VIVIENDAS CON ACCESO"] = d_con_agua
g_dist_agua["% VIVIENDAS SIN ACCESO"] = d_sin_agua

# Sort the data by "% VIVIENDAS CON ACCESO" for province chart
g_prov_agua = g_prov_agua.sort_values("% VIVIENDAS CON ACCESO")

# Transform the data for the main chart
folded_data = g_prov_agua.melt(
    id_vars=["PROVINCIA","POBLACION"],
    value_vars=["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"],
    var_name="Estado de acceso",
    value_name="Porcentaje"
)
folded_data["Porcentaje"] = folded_data["Porcentaje"].astype(float) / 100.0
# Create the main chart using Altair
chart = (
    alt.Chart(folded_data)
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
        tooltip=["Estado de acceso", alt.Tooltip("Porcentaje:Q", format=".2%"), "PROVINCIA", "POBLACION"],
    )
    .properties(
        title="BRECHAS A CUBRIR ACCESO A AGUA POTABLE POR PROVINCIA EN APURIMAC",
        width=600,
        height=400,
    )
)

# Show the main chart
st.altair_chart(chart, use_container_width=True)

# Sort the data by "% VIVIENDAS CON ACCESO" for district chart
g_dist_agua = g_dist_agua.sort_values("% VIVIENDAS CON ACCESO")

# Add a subheader and display the selected province's district bar chart
selected_province = st.selectbox("Seleccione una provincia", g_prov_agua["PROVINCIA"])
selected_province_data = g_dist_agua[g_dist_agua["PROVINCIA"] == selected_province]

st.subheader(f"Brecha de agua potable por cubrir en {selected_province}")
chart_data = pd.melt(selected_province_data, id_vars=["DISTRITO", "POBLACION"], value_vars=["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"], var_name="Estado de acceso", value_name="Porcentaje")
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
    tooltip=["Estado de acceso", alt.Tooltip("Porcentaje:Q", format=".2%"),"DISTRITO", "POBLACION"]
).properties(width=600, height=400)

st.altair_chart(bar_chart, use_container_width=True)
