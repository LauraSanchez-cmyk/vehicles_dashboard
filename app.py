import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Dashboard de vehículos",
    layout="wide"
)

st.title("Análisis de anuncios de vehículos usados")
st.write("Explora y compara anuncios de vehículos usados.")


# Cargar los datos
@st.cache_data
def load_data():
    data = pd.read_csv("vehicles_us.csv")

    # Obtener el fabricante a partir de la columna model
    data["manufacturer"] = (
        data["model"]
        .fillna("unknown")
        .astype(str)
        .str.strip()
        .str.split()
        .str[0]
        .str.lower()
    )

    data["price"] = pd.to_numeric(data["price"], errors="coerce")
    data["model_year"] = pd.to_numeric(
        data["model_year"], errors="coerce"
    )

    return data


car_data = load_data()


# 1. VISUALIZADOR DE DATOS
st.header("Data viewer")

include_small = st.checkbox(
    "Include manufacturers with less than 1000 ads",
    value=True
)

if include_small:
    table_data = car_data
else:
    manufacturer_counts = car_data["manufacturer"].value_counts()
    common_manufacturers = manufacturer_counts[
        manufacturer_counts >= 1000
    ].index

    table_data = car_data[
        car_data["manufacturer"].isin(common_manufacturers)
    ]

columns_to_show = [
    "manufacturer",
    "model_year",
    "cylinders",
    "fuel",
    "odometer",
    "transmission",
    "type",
    "paint_color",
    "is_4wd"
]

columns_available = [
    col for col in columns_to_show if col in table_data.columns
]

st.dataframe(
    table_data[columns_available].head(50),
    use_container_width=True
)


# 2. TIPOS DE VEHÍCULOS POR FABRICANTE
st.header("Vehicle types by manufacturer")

fig_types = px.histogram(
    car_data.dropna(subset=["manufacturer", "type"]),
    x="manufacturer",
    color="type",
    title="Vehicle types by manufacturer"
)

fig_types.update_layout(
    barmode="stack",
    xaxis_title="manufacturer",
    yaxis_title="count"
)

fig_types.update_xaxes(tickangle=-45)

st.plotly_chart(fig_types, use_container_width=True)


# 3. CONDICIÓN DEL VEHÍCULO POR AÑO DEL MODELO
st.header("Histogram of condition vs model_year")

fig_condition = px.histogram(
    car_data.dropna(subset=["model_year", "condition"]),
    x="model_year",
    color="condition",
    title="Histogram of condition vs model_year"
)

fig_condition.update_layout(
    xaxis_title="model_year",
    yaxis_title="count"
)

st.plotly_chart(fig_condition, use_container_width=True)


# 4. COMPARACIÓN DE PRECIOS ENTRE FABRICANTES
st.header("Compare price distribution between manufacturers")

manufacturers = sorted(
    car_data.loc[
        car_data["manufacturer"] != "unknown",
        "manufacturer"
    ].dropna().unique()
)

if len(manufacturers) >= 2:

    col1, col2 = st.columns(2)

    default_1 = (
        manufacturers.index("chevrolet")
        if "chevrolet" in manufacturers else 0
    )

    default_2 = (
        manufacturers.index("hyundai")
        if "hyundai" in manufacturers else 1
    )

    with col1:
        manufacturer_1 = st.selectbox(
            "Select manufacturer 1",
            manufacturers,
            index=default_1
        )

    with col2:
        manufacturer_2 = st.selectbox(
            "Select manufacturer 2",
            manufacturers,
            index=default_2
        )

    normalize = st.checkbox(
        "Normalize histogram",
        value=True
    )

    comparison_data = car_data[
        car_data["manufacturer"].isin(
            [manufacturer_1, manufacturer_2]
        )
    ].dropna(subset=["price"])

    fig_comparison = px.histogram(
        comparison_data,
        x="price",
        color="manufacturer",
        barmode="overlay",
        histnorm="percent" if normalize else None,
        opacity=0.6,
        title="Compare price distribution between manufacturers"
    )

    fig_comparison.update_layout(
        xaxis_title="price",
        yaxis_title="percent" if normalize else "count"
    )

    st.plotly_chart(fig_comparison, use_container_width=True)

else:
    st.warning("No hay suficientes fabricantes para comparar.")