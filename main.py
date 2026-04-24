import streamlit as st
import google.generativeai as genai

# Configuración de seguridad (Secrets)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("Error: Configura la API Key en los Secrets de Streamlit.")
    st.stop()

# --- INTERFAZ DE TU CALCULADORA BELOTTI ---
st.title("📊 Belotti Analytics")
st.subheader("Calculadora de Inversión Inmobiliaria")

# Aquí regresan tus campos de entrada
col1, col2 = st.columns(2)

with col1:
    precio = st.number_input("Precio de Venta (USD)", value=1150000)
    renta_mensual = st.number_input("Ingreso Mensual Bruto (USD)", value=19050)

with col2:
    mantenimiento = st.number_input("Gastos Mensuales (USD)", value=1000)
    ocupacion = st.slider("Porcentaje de Ocupación Anual", 0, 100, 70)

# Cálculos automáticos (Tu lógica de siempre)
ingreso_anual = (renta_mensual * 12) * (ocupacion / 100)
gastos_anuales = (mantenimiento * 12)
utilidad_neta = ingreso_anual - gastos_anuales
cap_rate = (utilidad_neta / precio) * 100

# Resultados grandes y claros
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Ingreso Anual", f"${ingreso_anual:,.2f}")
c2.metric("Utilidad Neta", f"${utilidad_neta:,.2f}")
c3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONSULTORÍA IA (Como un extra al final) ---
st.markdown("---")
st.subheader("🤖 Consultoría IA Belotti")
pregunta = st.text_input("¿Quieres un análisis de estos números?", placeholder="Ej: ¿Es este un buen negocio para el centro de Cancún?")

if st.button("Analizar con IA"):
    with st.spinner("Analizando..."):
        contexto = f"Antonio Belotti está analizando: Precio ${precio}, Renta Mensual ${renta_mensual}, Ocupación {ocupacion}%, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"
        response = model.generate_content(contexto)
        st.info(response.text)
