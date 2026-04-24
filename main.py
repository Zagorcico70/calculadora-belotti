import streamlit as st
import google.generativeai as genai

# --- 1. CONFIGURACIÓN DE IA ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
except Exception as e:
    st.error("Error de configuración. Verifica los Secrets en Streamlit.")
    st.stop()

# --- 2. INTERFAZ DE LA CALCULADORA ---
st.title("📊 Belotti Analytics")
st.subheader("Calculadora de Inversión Inmobiliaria")

col1, col2 = st.columns(2)

with col1:
    precio = st.number_input("Precio de Venta (USD)", value=1150000)
    renta_mensual = st.number_input("Ingreso Mensual Bruto (USD)", value=19050)

with col2:
    mantenimiento = st.number_input("Gastos Mensuales (USD)", value=1000)
    ocupacion = st.slider("Porcentaje de Ocupación Anual", 0, 100, 70)

# Lógica de cálculo
ingreso_anual = (renta_mensual * 12) * (ocupacion / 100)
gastos_anuales = (mantenimiento * 12)
utilidad_neta = ingreso_anual - gastos_anuales
cap_rate = (utilidad_neta / precio) * 100

# Resultados visuales
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Ingreso Anual", f"${ingreso_anual:,.2f}")
c2.metric("Utilidad Neta", f"${utilidad_neta:,.2f}")
c3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- 3. CONSULTORÍA IA (Corregido) ---
st.markdown("---")
st.subheader("🤖 Consultoría IA Belotti")

# Definimos la variable 'pregunta' ANTES de usarla
pregunta = st.text_input("¿Qué análisis necesitas sobre estos números?", placeholder="Ej: ¿Es este un buen ROI para Cancún?")

if st.button("Analizar con IA"):
    if pregunta: # Ahora sí existe la variable
        with st.spinner("Analizando con Belotti AI..."):
            try:
                prompt = f"Experto inmobiliario en Cancún. Analiza: Precio ${precio}, Renta Mensual ${renta_mensual}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.error("Error al generar la respuesta. Intenta de nuevo.")
    else:
        st.warning("Por favor, escribe una pregunta primero.")
