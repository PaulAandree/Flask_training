import streamlit as st
import pandas as pd
import altair as alt

df = pd.read_csv(r"E:\\_02_practicas_region_apurimac\\Tareas sub gerencia (David)\\Tarea_03 - indicadores\\Apurimac.csv", encoding='utf-8')

# Function to calculate "% VIVIENDAS CON ACCESO" and "% VIVIENDAS SIN ACCESO" columns
def calculate_access_percentage(df):
    a = round(df["VIVIENDAS CON LUZ"] / (df["VIVIENDAS CON LUZ"] + df["VIVIENDAS SIN LUZ"]) * 100, 2)
    b = 100 - a
    df["% VIVIENDAS CON ACCESO"] = a
    df["% VIVIENDAS SIN ACCESO"] = b
    return df

calculate_access_percentage(df)

rural_data = df[df['AREA'] == 'RURAL']
urbano_data = df[df['AREA'] == 'URBANO']

# Grouping and calculations for rural data
g_prov_rural = rural_data.groupby("PROVINCIA").sum().reset_index()
g_dist_rural = rural_data.groupby(["PROVINCIA", "DISTRITO"]).sum().reset_index()

a_p_rural = round(g_prov_rural["VIVIENDAS CON LUZ"] / (g_prov_rural["VIVIENDAS CON LUZ"] + g_prov_rural["VIVIENDAS SIN LUZ"]) * 100, 2)
b_p_rural = 100 - a_p_rural

a_d_rural = round(g_dist_rural["VIVIENDAS CON LUZ"] / (g_dist_rural["VIVIENDAS CON LUZ"] + g_dist_rural["VIVIENDAS SIN LUZ"]) * 100, 2)
b_d_rural = 100 - a_d_rural

g_prov_rural["% VIVIENDAS CON ACCESO"] = a_p_rural
g_prov_rural["% VIVIENDAS SIN ACCESO"] = b_p_rural
g_dist_rural["% VIVIENDAS CON ACCESO"] = a_d_rural
g_dist_rural["% VIVIENDAS SIN ACCESO"] = b_d_rural

# Grouping and calculations for urbano data
g_prov_urbano = urbano_data.groupby("PROVINCIA").sum().reset_index()
g_dist_urbano = urbano_data.groupby(["PROVINCIA", "DISTRITO"]).sum().reset_index()

a_p_urbano = round(g_prov_urbano["VIVIENDAS CON LUZ"] / (g_prov_urbano["VIVIENDAS CON LUZ"] + g_prov_urbano["VIVIENDAS SIN LUZ"]) * 100, 2)
b_p_urbano = 100 - a_p_urbano

a_d_urbano = round(g_dist_urbano["VIVIENDAS CON LUZ"] / (g_dist_urbano["VIVIENDAS CON LUZ"] + g_dist_urbano["VIVIENDAS SIN LUZ"]) * 100, 2)
b_d_urbano = 100 - a_d_urbano

g_prov_urbano["% VIVIENDAS CON ACCESO"] = a_p_urbano
g_prov_urbano["% VIVIENDAS SIN ACCESO"] = b_p_urbano
g_dist_urbano["% VIVIENDAS CON ACCESO"] = a_d_urbano
g_dist_urbano["% VIVIENDAS SIN ACCESO"] = b_d_urbano

# Function to display the selected dataframe
def display_data(selected_data):
    # Sort the data by "VIVIENDAS CON LUZ %" for province chart
    selected_data_prov = selected_data.groupby("PROVINCIA").sum().reset_index()
    selected_data_prov = selected_data_prov.sort_values("% VIVIENDAS CON ACCESO")
    
    # Create the main chart using Altair
    chart = (
        alt.Chart(selected_data_prov)
        .transform_fold(
            ["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"],
            as_=["Estado de acceso", "Porcentaje"],
        )
        .mark_bar()
        .encode(
            x=alt.X("Porcentaje:Q", stack="normalize", axis=alt.Axis(format=".2%")),
            y=alt.Y("PROVINCIA:N", sort="-x"),
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
            width=600,
            height=400,
        )
    )

    # Show the main chart
    st.altair_chart(chart, use_container_width=True)

    # Sort the data by "VIVIENDAS CON LUZ %_d" for district chart
    selected_data_dist = selected_data.groupby(["PROVINCIA", "DISTRITO"]).sum().reset_index()
    selected_data_dist = selected_data_dist.sort_values("% VIVIENDAS CON ACCESO")

    # Add a subheader and display the selected province's district bar chart
    selected_province = st.selectbox("Seleccione una provincia", selected_data_prov["PROVINCIA"])
    selected_province_data = selected_data_dist[selected_data_dist["PROVINCIA"] == selected_province]

    st.subheader(f"Brecha electrica a cubrir en {selected_province}")
    chart_data = pd.melt(
        selected_province_data,
        id_vars=["DISTRITO"],
        value_vars=["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"],
        var_name="Estado de acceso",
        value_name="Porcentaje"
    )
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

    #####################
    st.subheader(f"Brecha eléctrica a cubrir en {selected_province}")
    district_select = st.selectbox("Seleccione un distrito", selected_province_data["DISTRITO"])

    # Filter data based on selected district
    selected_district_data = selected_province_data[selected_province_data["DISTRITO"] == district_select]

    # Get the original district data for the selected district
    original_district_data = df[
        (df["PROVINCIA"] == selected_province) &
        (df["DISTRITO"] == district_select)
    ]

    # Display table for selected district
    table_data = original_district_data[["DISTRITO", "NOMBRE", "% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"]]

    # Format the columns with two decimal places
    table_data[["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"]] = table_data[["% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"]].applymap("{:.2f}".format)
    
    # Display the formatted table
    st.table(table_data)
    # Display table for selected district
    #st.table(original_district_data[["DISTRITO", "NOMBRE", "% VIVIENDAS CON ACCESO", "% VIVIENDAS SIN ACCESO"]])

# Sidebar selection
st.sidebar.header("Datos de acceso eléctrico")
area = st.sidebar.selectbox("Selecciona el área", ["RURAL", "URBANO"])
if area == "RURAL":
    display_data(g_dist_rural)
else:
    display_data(g_dist_urbano)

