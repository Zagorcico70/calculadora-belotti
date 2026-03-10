import streamlit as st

def check_password():
    if "password_correct" not in st.session_state:
        st.sidebar.title("🔐 Acceso Privado")
        # Aquí puedes cambiar el texto a español si quieres
        password = st.sidebar.text_input("Introduce el código para acceder:", type="password")
        if st.sidebar.button("Entrar"):
            if password == "Belotti2026": # <--- Esta es tu contraseña
                st.session_state["password_correct"] = True
                st.rerun()
  
# ESTA LÍNEA ES CLAVE:
if check_password():

    st.set_page_config(page_title="Belotti Inversiones", layout="centered")

locaciones = {
"Villas Marlin": [21.102437786454768, -86.76195352773082],
"Amara": [21.1685, -86.8010],
"Puerto Cancun": [21.16205146928014, -86.80774264339938],
"La Amada": [21.2585, -86.8115],
}


with st.sidebar:
    
    st.title("Configuración")
    prop = st.text_input("Propiedad / Cliente", value="Villas Marlin")
    pct_cierre = st.slider("Gastos de Cierre e Impuestos %", 5, 6, 7)


st.title(f"Análisis: {prop}")
col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio de Venta (USD)", value=250000, step=10000)
with col2:
    renta = st.number_input("Renta Mensual (USD)", value=2500, step=100)

inversion_total = precio * (1 + (pct_cierre / 100))
utilidad_neta_anual = (renta * 12) * 0.75  # Menos 20% de mantenimiento/administración
roi_final = (utilidad_neta_anual / inversion_total) * 100

# --- 1. ENTRADAS DE DATOS (INPUTS) ---
st.title("📊 Calculadora de Inversión Belotti")

# --- 1. ENTRADAS DE DATOS (Pon esto al principio de tu app) ---
st.title("📊 Calculadora de Inversión Belotti")

# (Aquí van tus sliders de precio y renta que ya tienes...)
precio = st.number_input("Precio de la Propiedad (USD)", value=1250000)
renta_mensual = st.number_input("Renta Mensual Estimada (USD)", value=6500)

# MOVER EL SELECTOR AQUÍ ARRIBA (Solo debe haber uno)
zona_mapa = st.selectbox("📍 Selecciona la ubicación estratégica:", 
                         ["Puerto Cancún (Blume/Shark/SLS)", 
                          "Zona Hotelera (Villas Marlin)", 
                          "Puerta del Mar (Amara)", 
                          "Playa Mujeres (La Amada)"])

# --- 2. LÓGICA DE DATOS (Solo una vez) ---
if "Puerto" in zona_mapa:
    lat, lon, zoom_mapa = 21.1415, -86.8042, 15
    lugar, plusvalia_num = "Puerto Cancún", 9.5
    perfil_txt = "💎 **Estrategia:** Preservación de Capital y Lujo."
elif "Marlin" in zona_mapa:
    lat, lon, zoom_mapa = 21.1410, -86.7628, 15
    lugar, plusvalia_num = "Villas Marlin", 6.0
    perfil_txt = "🏖️ **Estrategia:** Generación de Flujo de Efectivo."
elif "Amara" in zona_mapa:
    lat, lon, zoom_mapa = 21.1718, -86.8051, 15
    lugar, plusvalia_num = "Amara", 8.0
    perfil_txt = "⚓ **Estrategia:** Crecimiento Residencial Sólido."
elif "Amada" in zona_mapa:
    lat, lon, zoom_mapa = 21.2410, -86.8065, 15
    lugar, plusvalia_num = "La Amada", 11.0
    perfil_txt = "🚤 **Estrategia:** Plusvalía por Desarrollo."
else:
    lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1619, -86.8515, 12, "Cancún", 5.0
    perfil_txt = "Análisis general de mercado."

# --- 3. CÁLCULOS DE ROI (Asegúrate de que 'roi_porcentaje' esté bien definido) ---
roi_porcentaje = ((renta_mensual * 12) / precio) * 100
retorno_total = roi_porcentaje + plusvalia_num

# --- 4. RESULTADOS 360° (Solo una vez) ---
st.divider()
st.subheader(f"📈 Análisis de Inversión 360°: {lugar}")

col_met1, col_met2, col_met3 = st.columns(3)
with col_met1:
    st.metric("ROI (Renta)", f"{roi_porcentaje:.2f}%")
with col_met2:
    st.metric("Plusvalía Est.", f"{plusvalia_num}%")
with col_met3:
    st.metric("RETORNO TOTAL", f"{retorno_total:.2f}%", delta=f"+{plusvalia_num}% Apprec.")

st.info(perfil_txt)

# --- 5. MAPA ÚNICO ---
import pandas as pd
df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
st.map(df_mapa, zoom=zoom_mapa)

# --- 6. CONTACTO Y CIERRE (Solo una vez al final) ---
st.divider()
col_redes1, col_redes2 = st.columns(2)
with col_redes1:
    st.link_button("💬 WhatsApp", "https://wa.me/529983959242")
with col_redes2:
    st.link_button("🔗 Perfil LinkedIn", "https://www.linkedin.com/in/antonio-belotti-93521a8b/?locale=es")

st.caption(f"🗺️ [Abrir {lugar} en Google Maps](http://maps.google.com/?q={lat},{lon})")
st.caption("---")
st.caption("Antonio Belotti | Real Estate Data Analyst & Certified Agent")
st.caption("Certificación CONOCER: D-0012504124")
