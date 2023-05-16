import altair as alt
from vega_datasets import data
import pandas as pd

# Load the cars dataset from vega_datasets
data = pd.read_csv(
    r"E:\\_02_practicas_region_apurimac\\Tareas_sub gerente(David )\\Tarea_03 - indicadores\\Apurimac.csv"
)

grouped_by_provincia = data.groupby("PROVINCIA").sum().reset_index()
grouped_by_distrito = data.groupby(["PROVINCIA", "DISTRITO"]).sum().reset_index()

# Calculate percentages relative to the sum of "VIVIENDAS CON LUZ" and "VIVIENDAS SIN LUZ"
a_p = grouped_by_provincia["VIVIENDAS_CON_LUZ_PERCENT"] = round(
    (
        grouped_by_provincia["VIVIENDAS CON LUZ"]
        / (
            grouped_by_provincia["VIVIENDAS CON LUZ"]
            + grouped_by_provincia["VIVIENDAS SIN LUZ"]
        )
        * 100
    ),
    2,
)
b_p = grouped_by_provincia["VIVIENDAS_SIN_LUZ_PERCENT"] = (
    100 - grouped_by_provincia["VIVIENDAS_CON_LUZ_PERCENT"]
)

p_p = grouped_by_provincia["PROVINCIA"]

# Calculate percentages relative to the sum of "VIVIENDAS CON LUZ" and "VIVIENDAS SIN LUZ"
a = grouped_by_distrito["VIVIENDAS_CON_LUZ_PERCENT_d"] = round(
    (
        grouped_by_distrito["VIVIENDAS CON LUZ"]
        / (
            grouped_by_distrito["VIVIENDAS CON LUZ"]
            + grouped_by_distrito["VIVIENDAS SIN LUZ"]
        )
        * 100
    ),
    2,
)
b = grouped_by_distrito["VIVIENDAS_SIN_LUZ_PERCENT_d"] = (
    100 - grouped_by_distrito["VIVIENDAS_CON_LUZ_PERCENT_d"]
)

# Create an interactive scatter plot
chart = (
    alt.Chart(grouped_by_provincia)
    .mark_bar()
    .encode(
        x=alt.X("VIVIENDAS_CON_LUZ_PERCENT:Q"),
        y="PROVINCIA:O",
        color=("VIVIENDAS_CON_LUZ_PERCENT"),
        tooltip=["VIVIENDAS_CON_LUZ_PERCENT:Q"],
    )
    .properties(width=300, title="Viviendas con/sin Luz en Porcentaje")
)

chart += (
    alt.Chart(grouped_by_provincia)
    .mark_bar()
    .encode(
        x=alt.X("VIVIENDAS_SIN_LUZ_PERCENT"),
        y="PROVINCIA:O",
        color=alt.Color("VIVIENDAS_SIN_LUZ_PERCENT"),
        tooltip=["VIVIENDAS_SIN_LUZ_PERCENT:Q"],
    )
)

# Add a multi-selection event handler for the scatter plot
click = alt.selection_multi(fields=["PROVINCIA"])

# Apply the selection to the scatter plot
chart = chart.add_selection(click)

# Create a bar chart that displays the count of cars by Origin
bar = (
    alt.Chart(grouped_by_distrito)
    .mark_bar()
    .encode(
        x=alt.X("VIVIENDAS_CON_LUZ_PERCENT_d"),
        y="DISTRITO:N",
        color=("VIVIENDAS_SIN_LUZ_PERCENT_d"),
        tooltip=[
            "DISTRITO",
            "VIVIENDAS_CON_LUZ_PERCENT_d",
            "VIVIENDAS_SIN_LUZ_PERCENT_d",
        ],
    )
    .transform_filter(click)
)

# Combine the scatter plot and bar chart using a horizontal layout
chart = alt.hconcat(chart, bar)

# Display the chart
chart
