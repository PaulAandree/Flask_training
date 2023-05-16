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
df = df.dropna()


########################## si funciona, sin porcentages
# Streamlit app
st.title("Reporte de Datos")

# Button for grouping by provincia
if st.button("Agrupar por provincia"):
    grouped_by_provincia = df.groupby("PROVINCIA").sum().reset_index()

    # Create an interactive chart using altair
    chart = (
        alt.Chart(grouped_by_provincia)
        .mark_bar()
        .encode(
            x="PROVINCIA",
            y="VIVIENDAS CON LUZ",
            tooltip=["PROVINCIA"],  # Add the "PROVINCIA" column to the tooltip
        )
        .interactive()
    )

    # Display the chart using Streamlit
    st.altair_chart(chart, use_container_width=True)

    st.area_chart(grouped_by_provincia[["VIVIENDAS SIN LUZ", "VIVIENDAS CON LUZ"]])

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
            tooltip=["DISTRITO"],  # Add the "DISTRITO" column to the tooltip
        )
        .interactive()
    )

    # Display the chart using Streamlit
    st.altair_chart(chart, use_container_width=True)

    st.area_chart(grouped_by_district[["VIVIENDAS SIN LUZ", "VIVIENDAS CON LUZ"]])

# Button for grouping by name
if st.button("Agrupar por Nombre"):
    grouped_by_name = df.groupby("NOMBRE").sum().reset_index()
    # st.table(grouped_by_name)
    st.area_chart(grouped_by_name[["VIVIENDAS SIN LUZ", "VIVIENDAS CON LUZ"]])

# Select rural or urban area
area_filter = st.radio("Seleccionar Área", ["RURAL", "URBANO"])
filtered_data = df[df["AREA"] == area_filter]
# st.table(filtered_data)
st.area_chart(filtered_data[["VIVIENDAS SIN LUZ", "VIVIENDAS CON LUZ"]])


##############################
# Select provinces of the department
area_filter = st.radio("Seleccionar provinc", df["PRoVINCIA"].unique().tolist())
filtered_data = df[df["AREA"] == area_filter]
# st.table(filtered_data)
st.area_chart(filtered_data[["VIVIENDAS SIN LUZ", "VIVIENDAS CON LUZ"]])
# @st.cache # stores caches of the app


###############################
# Button for grouping by district
if st.button("Agrupar por Distrito"):
    grouped_by_district = df.groupby("DISTRITO").sum().reset_index()

    # Calculate percentages relative to the sum of "VIVIENDAS CON LUZ" and "VIVIENDAS SIN LUZ"
    grouped_by_district["VIVIENDAS_CON_LUZ_PERCENT"] = (
        grouped_by_district["VIVIENDAS CON LUZ"]
        / (
            grouped_by_district["VIVIENDAS CON LUZ"]
            + grouped_by_district["VIVIENDAS SIN LUZ"]
        )
        * 100
    )
    grouped_by_district["VIVIENDAS_SIN_LUZ_PERCENT"] = (
        100 - grouped_by_district["VIVIENDAS_CON_LUZ_PERCENT"]
    )

    # Create an interactive chart using altair
    chart = (
        alt.Chart(grouped_by_district)
        .mark_bar()
        .encode(
            x="DISTRITO",
            y=alt.Y("VIVIENDAS_CON_LUZ_PERCENT:Q"),
            tooltip=[
                "DISTRITO",
                "VIVIENDAS_CON_LUZ_PERCENT",
                "VIVIENDAS_SIN_LUZ_PERCENT",
            ],
        )
        .interactive()
    )

    # Display the chart using Streamlit
    st.altair_chart(chart, use_container_width=True)


### SI FUNCIONA ############ it displays only the province when clic

import streamlit as st
import altair as alt
import pandas as pd

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


#################################### noooo funciona mas tentivo
# Streamlit app
st.title("Reporte de Datos")

# Group data by district and province
grouped_by_district = df.groupby(["DISTRITO", "PROVINCIA"]).sum().reset_index()
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
click = alt.selection_multi(fields=["PROVINCIA"], bind="legend")

# Apply the event handler to the chart
chart = chart.add_selection(click)

# Handle the click event and update the chart
if chart:
    # Get the selected provinces
    selected_provinces = click["PROVINCIA"]

    # Filter the data based on the selected provinces
    filtered_data = grouped_by_district[
        grouped_by_district["PROVINCIA"].isin(selected_provinces)
    ]

    # Create a new chart with the filtered data
    filtered_chart = (
        alt.Chart(filtered_data)
        .mark_bar()
        .encode(
            x="DISTRITO",
            y=alt.Y("VIVIENDAS_CON_LUZ_PERCENT:Q"),
            tooltip=[
                "DISTRITO",
                "PROVINCIA",
                "VIVIENDAS_CON_LUZ_PERCENT",
                "VIVIENDAS_SIN_LUZ_PERCENT",
            ],
        )
    )

    # Display the filtered chart using Streamlit
    st.altair_chart(filtered_chart, use_container_width=True)
else:
    # Display the initial chart using Streamlit
    st.altair_chart(chart, use_container_width=True)

# Select rural or urban area
area_filter = st.radio("Seleccionar Área", ["RURAL", "URBANO"])
filtered_data = df[df["AREA"] == area_filter]
st.area_chart(filtered_data[["VIVIENDAS SIN LUZ", "VIVIENDAS CON LUZ"]])
