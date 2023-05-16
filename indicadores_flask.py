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

g_prov["VIVIENDAS CON LUZ %"]   = a_p.astype(str)
g_prov["VIVIENDAS SIN LUZ %"]   = b_p.astype(str)
g_dist["VIVIENDAS CON LUZ %_d"] = a_d.astype(str)
g_dist["VIVIENDAS SIN LUZ %_d"] = b_d.astype(str)

# Create the chart using Altair
chart = (
    alt.Chart(g_prov)
    .transform_fold(
        ["VIVIENDAS CON LUZ %", "VIVIENDAS SIN LUZ %"],
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
                domain=["VIVIENDAS CON LUZ %", "VIVIENDAS SIN LUZ %"],
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

# Add a multi-selection event handler for the scatter plot
click = alt.selection_multi(fields=["PROVINCIA"])

# Apply the selection to the scatter plot
chart = chart.add_selection(click)

# Create a bar chart that displays the districts 
bar = (
    alt.Chart(g_dist)
    .transform_fold(
        ["VIVIENDAS CON LUZ %", "VIVIENDAS SIN LUZ %"],
        as_=["Estado de acceso", "Porcentaje"],
    )
    .mark_bar()
    .encode(
        y=alt.Y("DISTRITO:N", sort="-x"),
        x=alt.X("Porcentaje:Q", stack="normalize", axis=alt.Axis(format=".2%")),
        color=alt.Color(
            "Estado de acceso:N",
            legend=alt.Legend(title="Estado de acceso"),
            scale=alt.Scale(
                domain=["VIVIENDAS CON LUZ %", "VIVIENDAS SIN LUZ %"],
                range=["#50B4C7", "#ED7D31"],)
        )
        
).transform_filter(click)
)

combined_chart = alt.hconcat(chart, bar)

#show it on stremlit
st.altair_chart(combined_chart, use_container_width=True)
