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

---------------------------------------------------------
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
        x=alt.X("Porcentaje:Q", stack="normalize", axis=alt.Axis(format=".2%"))
        
).transform_filter(click)
)

combined_chart = alt.hconcat(chart, bar)

#show it on stremlit
st.altair_chart(combined_chart, use_container_width=True)

st.write(g_dist[g_dist["PROVINCIA"]== "ABANCAY"])
#
# ---------------------------------LEAN STUFF-------------------------------------

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


# ---------------------------------BUTTON[CHUNKY STUFF].SAVE AS PNG-------------------------------------
# ---------------------almost there------------------------
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define the data
data = pd.read_csv(r"E:\\_02_practicas_region_apurimac\\Tareas_sub gerente(David )\\Tarea_03 - indicadores\\Apurimac.csv")

g_prov = data.groupby("PROVINCIA").sum().reset_index()
g_dist = data.groupby(["PROVINCIA", "DISTRITO"]).sum().reset_index()

a_p = round(g_prov["VIVIENDAS CON LUZ"] / (g_prov["VIVIENDAS CON LUZ"] + g_prov["VIVIENDAS SIN LUZ"]) * 100, 2)
b_p = 100 - a_p

a_d = round(g_dist["VIVIENDAS CON LUZ"] / (g_dist["VIVIENDAS CON LUZ"] + g_dist["VIVIENDAS SIN LUZ"]) * 100, 2)
b_d = 100 - a_d

g_prov["% VIVIENDAS CON ACCESO"] = a_p.astype(str)
g_prov["% VIVIENDAS SIN ACCESO"] = b_p.astype(str)
g_dist["% VIVIENDAS CON ACCESO"] = a_d.astype(str)
g_dist["% VIVIENDAS SIN ACCESO"] = b_d.astype(str)

# Sort the data by "% VIVIENDAS CON ACCESO" for province chart
g_prov = g_prov.sort_values("% VIVIENDAS CON ACCESO")


## option that saves this charts as .png files
# Create the main province bar chart
fig, ax = plt.subplots(figsize=(7.5,6))
province_bars = ax.barh(g_prov["PROVINCIA"], g_prov["% VIVIENDAS CON ACCESO"].astype(float),
                        color="#50B4C7", label="% VIVIENDAS CON ACCESO")
ax.barh(g_prov["PROVINCIA"], g_prov["% VIVIENDAS SIN ACCESO"].astype(float),
        left=g_prov["% VIVIENDAS CON ACCESO"].astype(float), color="#ED7D31", label="% VIVIENDAS SIN ACCESO")

# Add percentage labels to the province bars
for (bar_con, bar_sin) in zip(province_bars, ax.patches[len(province_bars):]):
    width_con = bar_con.get_width()
    width_sin = bar_sin.get_width() +100
    x_con = width_con - 35
    x_sin = width_sin
    y_con = bar_con.get_y() + bar_con.get_height() / 2
    y_sin = bar_sin.get_y() + bar_sin.get_height() / 2
    ax.text(x_con, y_con, f"{width_con:.1f}%", ha="center", va="center")
    ax.text(x_sin, y_sin, f"{width_sin:.1f}%", ha="center", va="center")

st.write(g_prov["% VIVIENDAS CON ACCESO"])

# Configure the chart appearance
ax.set_xlabel("Porcentaje")
ax.set_ylabel("Provincia")
ax.set_title("BRECHAS A CUBRIR EN FLUIDO ELECTRICO POR PROVINCIA EN APURIMAC")
ax.legend()
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

# Display the province bar chart
st.pyplot(fig)

# Add a subheader and display the selected province's district bar chart
selected_province = st.selectbox("Select a province", g_prov["PROVINCIA"])
selected_province_data = g_dist[g_dist["PROVINCIA"] == selected_province].copy()
selected_province_data = selected_province_data.sort_values("% VIVIENDAS CON ACCESO")

# Create the district bar chart
fig, ax = plt.subplots()
district_bars = ax.barh(selected_province_data["DISTRITO"], selected_province_data["% VIVIENDAS CON ACCESO"].astype(float),
                        color="#50B4C7", label="% VIVIENDAS CON ACCESO")
ax.barh(selected_province_data["DISTRITO"], selected_province_data["% VIVIENDAS SIN ACCESO"].astype(float),
        left=selected_province_data["% VIVIENDAS CON ACCESO"].astype(float), color="#ED7D31", label="% VIVIENDAS SIN ACCESO")

# Add percentage labels to the district bars
for bar_con, bar_sin in zip(district_bars, ax.patches[len(district_bars):]):
    width_con = bar_con.get_width()
    width_sin = bar_sin.get_width()
    x_con = width_con + 1
    x_sin = width_sin + 1
    y_con = bar_con.get_y() + bar_con.get_height() / 2
    y_sin = bar_sin.get_y() + bar_sin.get_height() / 2
    ax.text(x_con, y_con, f"{width_con:.1f}%", ha="center", va="center")
    ax.text(x_sin, y_sin, f"{width_sin:.1f}%", ha="center", va="center")

# Configure the chart appearance
ax.set_xlabel("Porcentaje")
ax.set_ylabel("Distrito")
ax.set_title(f"BRECHAS A CUBRIR EN FLUIDO ELECTRICO EN DISTRITOS DE {selected_province}")
ax.legend()
plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1))

# Display the district bar chart
st.pyplot(fig)

#                                     THE 'BUTTON' -TO BE FIXED                              #

def save_chart_as_png(chart, filename):
    altair_saver.save(chart, filename)

# Display the chart
st.altair_chart(chart, use_container_width=True)

# Add a button to save the chart as PNG
if st.button("Save Chart as PNG"):
    filename = "chart.png"  # You can customize the filename if desired
    save_chart_as_png(chart, filename)
    st.success(f"Chart saved as {filename}")

# ... your existing code ...

# Display the bar chart
st.altair_chart(bar_chart, use_container_width=True)

# Add a button to save the bar chart as PNG
if st.button("Save Bar Chart as PNG"):
    filename = "bar_chart.png"  # You can customize the filename if desired
    save_chart_as_png(bar_chart, filename)
    st.success(f"Bar chart saved as {filename}")









    #-----------------------AGUA POTABLE - FUNCIONA --------------------------------#
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

# Sort the data by "VIVIENDAS CON AGUA %" for province chart
g_prov_agua = g_prov_agua.sort_values("% VIVIENDAS CON ACCESO")

# Create the main chart using Altair
chart = (
    alt.Chart(g_prov_agua)
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
        #tooltip=["Estado de acceso", alt.Tooltip("Porcentaje:Q", format=".2%"), "PROVINCIA", "POBLACION"],
    )
    .properties(
        title="BRECHAS A CUBRIR ACCESO A AGUA POTABLE POR PROVINCIA EN APURIMAC",
        width=600,
        height=400,
    )
)

# Show the main chart
st.altair_chart(chart, use_container_width=True)

# Sort the data by "VIVIENDAS CON LUZ %_d" for district chart
g_dist_agua = g_dist_agua.sort_values("% VIVIENDAS CON ACCESO")

# Add a subheader and display the selected province's district bar chart
selected_province = st.selectbox("Seleccione una provincia", g_prov_agua["PROVINCIA"])
selected_province_data = g_dist_agua[g_dist_agua["PROVINCIA"] == selected_province]

st.subheader(f"Brecha de agua potable por cubrir en {selected_province}")
chart_data = pd.melt(selected_province_data, id_vars=["DISTRITO","POBLACION"], value_vars=["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"], var_name="Estado de acceso", value_name="Porcentaje")
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
    order=alt.Order("Estado de acceso:N"),
    tooltip=["Estado de acceso", alt.Tooltip("Porcentaje:Q", format=".2%"), "DISTRITO", "POBLACION"]
).properties(width=600, height=400)

st.altair_chart(bar_chart, use_container_width=True)



    