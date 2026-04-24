import streamlit as st
import google.generativeai as genai

# 1. Configuración de la Página
st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# 2. Configuración Segura de la IA
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Falta la clave API en los Secrets de Streamlit.")
    st.stop()

# 3. Interfaz de la Calculadora
st.title("📊 Belotti Analytics")
st.subheader("Investment Calculator")

col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio de Venta (USD)", value=1150000.0)
    renta_mensual = st.number_input("Ingreso Mensual Bruto (USD)", value=19050.0)
with col2:
    mantenimiento = st.number_input("Gastos Mensuales (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación Anual %", 0, 100, 70)

# Cálculos
ingreso_anual = (renta_mensual * 12) * (ocupacion / 100)
utilidad_neta = ingreso_anual - (mantenimiento * 12)
cap_rate = (utilidad_neta / precio) * 100 if precio > 0 else 0

# Métricas
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Ingreso Anual", f"${ingreso_anual:,.2f}")
c2.metric("Utilidad Neta", f"${utilidad_neta:,.2f}")
c3.metric("CAP RATE", f"{cap_rate:.2f}%")

# 4. Consultoría IA
st.markdown("---")
st.subheader("🤖 Belotti AI Consulting")
pregunta = st.text_input("Haz tu consulta técnica aquí:")

if st.button("Analizar con IA"):
    if pregunta:
        with st.spinner("Generando análisis..."):
            try:
                # Prompt directo para evitar errores de codificación
                full_prompt = f"Eres un experto en Real Estate en Cancún. Analiza estos datos: Precio ${precio}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"
                response = model.generate_content(full_prompt)
                st.info(response.text)
            except Exception as e:
                st.error(f"Error de conexión con la IA. Detalle: {e}")
    else:
        st.warning("Por favor, escribe una pregunta.")
