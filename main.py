import streamlit as st
import pandas as pd

st.title("📊 Calculadora de Inversión Belotti")


precio = st.number_input("Precio de la Propiedad (USD)", value=1250000)
renta_mensual = st.number_input("Renta Mensual Estimada (USD)", value=6500)

zona_mapa = st.selectbox("📍 Ubicación:", ["Puerto Cancún...", "Villas Marlin...", "Amara...", "La Amada"])

# PASO 2: Inputs del Sidebar (Gastos)
st.sidebar.header("📉 Gastos Estimados")
mantenimiento_anual = st.sidebar.number_input("Mantenimiento Anual (USD)", value=5000)
predial_anual = st.sidebar.number_input("Predial Anual (USD)", value=800)


if "Puerto" in zona_mapa:
    lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1415, -86.8042, 15, "Puerto Cancún", 9.5
    perfil_txt = "💎 **Estrategia:** Preservación de Capital."
elif "Marlin" in zona_mapa:
    lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1410, -86.7628, 15, "Villas Marlin", 6.0
    perfil_txt = "🏖️ **Estrategia:** Cash Flow Turístico."
# ... (Sigue con tus otros 'elif' de Amara y Amada igual que antes) ...
else:
    lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1619, -86.8515, 12, "Cancún", 5.0
    perfil_txt = "Análisis general."


renta_anual_bruta = renta_mensual * 12
renta_neta_anual = renta_anual_bruta - mantenimiento_anual - predial_anual
gastos_escrituracion = precio * 0.05
inversion_total = precio + gastos_escrituracion

roi_porcentaje = (renta_neta_anual / inversion_total) * 100
retorno_total = roi_porcentaje + plusvalia_num


st.divider()
st.subheader(f"📈 Resultados: {lugar}")

col1, col2, col3 = st.columns(3)
col1.metric("ROI NETO", f"{roi_porcentaje:.2f}%")
col2.metric("Plusvalía", f"{plusvalia_num}%")
col3.metric("RETORNO TOTAL", f"{retorno_total:.2f}%")

st.info(perfil_txt)

# Mapa
df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
st.map(df_mapa, zoom=zoom_mapa)


st.divider()
st.subheader("📩 Contacto Directo")

col_redes1, col_redes2 = st.columns(2)

with col_redes1:
    st.write("¿Deseas una proyección personalizada de esta u otra propiedad?")
    st.link_button("💬 Enviar WhatsApp", "https://wa.me/529983959242")

with col_redes2:
    st.write("Sígueme para más análisis de datos inmobiliarios en Cancún:")
    st.link_button("🔗 Perfil de LinkedIn", "https://www.linkedin.com/in/antonio-belotti-93521a8b/")

# Pie de página profesional
st.write("---")
st.caption("🚀 **Antonio Belotti** | Real Estate Data Analyst & Certified Agent")
st.caption("📜 Certificación CONOCER: **D-0012504124**")
st.caption("📍 Cancún, Quintana Roo, México")


