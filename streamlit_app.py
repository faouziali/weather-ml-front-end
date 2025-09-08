import streamlit as st
import pandas as pd
import requests

# ---- Header ----
st.title("🌦️ Dashboard Weather ML")
st.subheader("Suivi des températures et prédictions avec Machine Learning")

# ---- Sidebar Filters ----
st.sidebar.header("Filtres")
selected_year = st.sidebar.selectbox("Année", [2023, 2024, 2025])
selected_month = st.sidebar.selectbox("Mois", list(range(1, 13)))
selected_day = st.sidebar.selectbox("Jour", list(range(1, 32)))

# ---- API call ----
API_URL = "http://159.89.179.82:8000/archive"
params = {
    "year": selected_year,
    "month": selected_month,
    "day": selected_day,
    "page_size": 24  # fixe
}

try:
    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    result = response.json()
    
    # Charger les données dans DataFrame
    data = pd.DataFrame(result['data'])
    
    # KPIs
    kpis = result.get('kpis', {})
    cloudy_days = kpis.get('cloudy_days', 0)
    rainy_hours = kpis.get('rainy_hours', 0.0)
    
except Exception as e:
    st.error(f"Erreur lors de la récupération des données API : {e}")
    data = pd.DataFrame()
    cloudy_days = 0
    rainy_hours = 0.0

# ---- Calcul de la précision du modèle ----
if not data.empty and "temperature_actual" in data.columns and "predicted_temperature_2m" in data.columns:
    # éviter division par zéro
    mask = data["temperature_actual"] != 0
    precision = ((1 - abs(data.loc[mask, "predicted_temperature_2m"] - data.loc[mask, "temperature_actual"]) / data.loc[mask, "temperature_actual"]).mean()) * 100
    precision = round(precision, 2)
else:
    precision = None

# ---- KPIs Display ----
col1, col2, col3 = st.columns(3)
col1.metric("🌧️ Heures de pluie", f"{rainy_hours} h")
col2.metric("☁️ Jours nuageux", f"{cloudy_days} j")
col3.metric("📈 Précision modèle", f"{precision}%" if precision is not None else "N/A")

# ---- Graph Display ----
if not data.empty:
    # S'assurer que les colonnes existent
    for col in ["temperature_actual", "predicted_temperature_2m"]:
        if col not in data.columns:
            data[col] = None

    # Renommer pour affichage graphique
    graph_df = data.rename(columns={"predicted_temperature_2m": "temperature_predicted"})
    st.subheader("📈 Température réelle vs prédite")
    st.line_chart(graph_df.set_index("time")[["temperature_actual", "temperature_predicted"]])

    # ---- Detailed Table ----
    st.subheader("📊 Données horaires détaillées")
    st.dataframe(data)

else:
    st.info("Aucune donnée disponible pour la sélection.")



