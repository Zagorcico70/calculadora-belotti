import streamlit as st
import pandas as pd

st.set_page_config(page_title="Belotti Premium", layout="centered")


locaciones = {
"Villas Marlin": [21.102437786454768, -86.76195352773082],
"Amara": [21.1685, -86.8010],
"Puerto Cancun": [21.1743, -86.8041],
"La Amada": [21.2585, -86.8115],
}


with st.sidebar:
    lang = st.selectbox("🌐", ["Español", "Italiano", "English"])
    prop = st.text_input("Propiedad", value="Villas Marlin")


st.title(f"Análisis: {prop}")
col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio USD", value=250000)
with col2:
    renta = st.number_input("Renta USD", value=2500)

roi = ((renta * 12 * 0.75) / precio) * 100
st.metric("ROI ESTIMADO", f"{roi:.2f}%")


st.subheader("Ubicación de la Inversión")
if prop in locaciones:
    punto = locaciones[prop]
    zoom_n = 15
else:
    punto = [21.1619, -86.8515]
    zoom_n = 12

df_mapa = pd.DataFrame({'lat': [punto[0]], 'lon': [punto[1]]})
st.map(df_mapa, zoom=16)
st.link_button("📍 Abrir Google Maps", f"https://www.google.com/maps?q={punto[0]},{punto[1]}")


st.divider()
c_btn1, c_btn2 = st.columns(2)

wa_link = f"https://wa.me/529847454906?text=Info%20sobre%20{prop}"


with c_btn1:
    st.link_button("📲 WhatsApp", wa_link, use_container_width=True)
with c_btn2:
    st.link_button("💼 Mi Perfil", "", use_container_width=True)
    st.caption("Antonio Belotti - Real Estate Advisor")
