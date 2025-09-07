import streamlit as st
import pandas as pd
import numpy as np
import datetime

# ---- Header ----
st.title("🌦️ Dashboard Weather ML")
st.subheader("Suivi des températures et prédictions avec Machine Learning")

# ---- Filters ----
st.sidebar.header("Filtres")
selected_year = st.sidebar.selectbox("Année", [2023, 2024, 2025])
selected_month = st.sidebar.selectbox("Mois", list(range(1, 13)))
selected_day = st.sidebar.selectbox("Jour", list(range(1, 32)))

# ---- KPIs ----
col1, col2, col3 = st.columns(3)
col1.metric("🌧️ Heures de pluie", "42 h", "+5%")
col2.metric("☁️ Jours nuageux", "120 j", "-3%")
col3.metric("📈 Précision modèle", "92%", "+1%")

# ---- Simulated Temperature Data ----
date_rng = pd.date_range(
    start=datetime.datetime(selected_year, selected_month, 1),
    periods=24,
    freq="H"
)

data = pd.DataFrame({
    "datetime": date_rng,
    "relative_humidity_2m": np.random.randint(50, 90, size=(24)),
    "dew_point_2m": np.random.uniform(10, 20, size=(24)),
    "wind_speed_10m": np.random.uniform(1, 5, size=(24)),
    "wind_direction_10m": np.random.randint(0, 360, size=(24)),
    "surface_pressure": np.random.uniform(1005, 1015, size=(24)),
    "cloud_cover": np.random.randint(0, 100, size=(24)),
    "precipitation": np.random.randint(0, 10, size=(24)),
})

# Ajout colonnes Actual vs Predicted
data["temperature_actual"] = np.random.uniform(15, 30, size=(24))
data["temperature_predicted"] = data["temperature_actual"] + np.random.normal(0, 1, size=(24))

# ---- Graph ----
st.line_chart(data.set_index("datetime")[["temperature_actual", "temperature_predicted"]])

# ---- Table ----
st.write("### 📊 Données horaires détaillées")
st.dataframe(data)


