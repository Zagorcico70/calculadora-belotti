import streamlit as st
import pandas as pd

st.set_page_config(page_title="Belotti Premium Real Estate", page_icon="🏢", layout="centered")

languages = {
"Español": {
"title": "Inversiones Belotti Cancún",
"subtitle": "Calculadora de ROI y Análisis de Zona",
"price": "Precio de Venta (USD)",
"rent": "Renta Mensual (USD)",
"expenses": "% Gastos Operativos",
"utilidad": "Utilidad Neta Anual",
"roi": "ROI Estimado",
"map_title": "Puntos de Interés en Cancún",
"contact": "Contactar por WhatsApp"
},
"Italiano": {
"title": "Investimenti Belotti Cancún",
"subtitle": "Calcolatore ROI e Analisi di Zona",
"price": "Prezzo di Vendita (USD)",
"rent": "Affitto Mensile (USD)",
"expenses": "% Spese Operative",
"utilidad": "Utile Netto Annuale",
"roi": "ROI Stimato",
"map_title": "Punti di Interesse a Cancún",
"contact": "Contatta su WhatsApp"
},
"English": {
"title": "Belotti Investments Cancún",
"subtitle": "ROI Calculator & Area Analysis",
"price": "Sale Price (USD)",
"rent": "Monthly Rent (USD)",
"expenses": "% Operating Expenses",
"utilidad": "Annual Net Profit",
"roi": "Estimated ROI",
"map_title": "Investment Hotspots in Cancún",
"contact": "Contact via WhatsApp"
}
}

with st.sidebar:
  
    st.header("🌐 Language")
    lang_choice = st.selectbox("Selecciona:", ["Español", "Italiano", "English"])
    text = languages[lang_choice]

st.title(text["title"])
st.markdown(f"{text['subtitle']}")

col_in1, col_in2 = st.columns(2)
with col_in1:
precio = st.number_input(text["price"], value=250000, step=10000)
with col_in2:
renta = st.number_input(text["rent"], value=2500, step=100)

gastos_pct = st.slider(text["expenses"], 10, 40, 25)

utilidad_neta = (renta * 12) * (1 - (gastos_pct / 100))
roi = (utilidad_neta / precio) * 100

st.divider()
c1, c2 = st.columns(2)
c1.metric(text["utilidad"], f"${utilidad_neta:,.0f}")
c2.metric(text["roi"], f"{roi:.2f}%")

st.subheader(text["map_title"])
map_data = pd.DataFrame({'lat': [21.1743, 21.1378], 'lon': [-86.8041, -86.7475]})
st.map(map_data)

st.divider()
st.link_button(text["contact"], "")
st.caption("Antonio Belotti - Certificado CONOCER D-0012504124")
