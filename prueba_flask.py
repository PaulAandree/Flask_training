import streamlit as st
import pandas as pd
import altair as alt

# Sample data
data = pd.read_csv(
    r"E:\\_02_practicas_region_apurimac\\Tareas_sub gerente(David )\\Tarea_03 - indicadores\\Apurimac.csv"
)

df = pd.DataFrame(
    data,
    columns=[
        "UBIGEO",
        "NOMBRE",
        "DEPARTAMENTO",
        "PROVINCIA",
        "DISTRITO",
        "POBLACION",
        "VIVIENDA",
        "VIVIENDAS CON LUZ",
        "VIVIENDAS SIN LUZ",
        "AREA",
    ],
)

# Streamlit app
st.title("Reporte de Datos")

# Button for grouping by provincia
if st.button("Agrupar por provincia"):
    grouped_by_provincia = df.groupby("PROVINCIA").sum().reset_index()

    # Calculate percentages relative to the sum of "VIVIENDAS CON LUZ" and "VIVIENDAS SIN LUZ"
    grouped_by_provincia["VIVIENDAS_CON_LUZ_PERCENT"] = (
        grouped_by_provincia["VIVIENDAS CON LUZ"]
        / (
            grouped_by_provincia["VIVIENDAS CON LUZ"]
            + grouped_by_provincia["VIVIENDAS SIN LUZ"]
        )
        * 100
    )
    grouped_by_provincia["VIVIENDAS_SIN_LUZ_PERCENT"] = (
        100 - grouped_by_provincia["VIVIENDAS_CON_LUZ_PERCENT"]
    )

    # Create an interactive chart using altair
    chart = (
        alt.Chart(grouped_by_provincia)
        .mark_bar()
        .encode(
            x="PROVINCIA",
            y=alt.Y("VIVIENDAS_CON_LUZ_PERCENT:Q"),
            tooltip=[
                "PROVINCIA",
                "VIVIENDAS_CON_LUZ_PERCENT",
                "VIVIENDAS_SIN_LUZ_PERCENT",
            ],
        )
    )

    # Add an event handler for bar clicks
    click = alt.selection_multi(fields=["PROVINCIA"])

    # Apply the event handler to the chart
    chart = chart.add_selection(click)

    # Handle the click event and update the chart
    filtered_chart = chart.transform_filter(click)

    # Display the chart using Streamlit
    st.altair_chart(filtered_chart, use_container_width=True)

# Select rural or urban area
area_filter = st.radio("Seleccionar Área", ["RURAL", "URBANO"])
filtered_data = df[df["AREA"] == area_filter]
st.area_chart(filtered_data[["VIVIENDAS SIN LUZ", "VIVIENDAS CON LUZ"]])

# Button for grouping by district
if st.button("Agrupar por Distrito"):
    grouped_by_district = df.groupby("DISTRITO").sum().reset_index()
    # st.table(grouped_by_district)

    # Create an interactive chart using altair
    chart = (
        alt.Chart(grouped_by_district)
        .mark_bar()
        .encode(
            x="DISTRITO",
            y="VIVIENDAS CON LUZ",
            color= (["VIVIENDAS_CON_LUZ_PERCENT_d","VIVIENDAS_SIN_LUZ_PERCENT_d"]),
            tooltip=["DISTRITO"],  # Add the "DISTRITO" column to the tooltip
        )
        .interactive()
    )

    # Display the chart using Streamlit
    st.altair_chart(chart, use_container_width=True)

    st.area_chart(grouped_by_district[["VIVIENDAS SIN LUZ", "VIVIENDAS CON LUZ"]])

area_filter = st.radio("Seleccionar Área", ["RURAL", "URBANO"])
filtered_data = df[df["AREA"] == area_filter]
# st.table(filtered_data)
st.area_chart(filtered_data[["VIVIENDAS SIN LUZ", "VIVIENDAS CON LUZ"]])
# @st.cache # stores caches of the app

# ask gpt: is it possible to pre process filtered data into the buttons to display in the flask app with this code: ?
