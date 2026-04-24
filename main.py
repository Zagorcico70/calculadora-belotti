import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- 1. CONFIGURACIÓN DE IA ---
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Usamos gemini-pro que es el más estable para evitar el error 404
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error al configurar IA: {e}")
else:
    st.error("⚠️ Falta la clave API en los Secrets de Streamlit.")
    st.stop()

# --- 2. INTERFAZ DE CALCULADORA ---
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

# Métricas Visuales
st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Ingreso Anual", f"${ingreso_anual:,.2f}")
c2.metric("Utilidad Neta", f"${utilidad_neta:,.2f}")
c3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- 3. CONSULTORÍA IA ---
st.markdown("---")
st.subheader("🤖 Belotti AI Consulting")

# PRIMERO creamos la caja de texto
pregunta_usuario = st.text_input("Haz tu consulta técnica aquí:", key="input_ia")

# LUEGO el botón que usa esa pregunta
if st.button("Analizar con IA"):
    if pregunta_usuario:
        with st.spinner("Generando análisis..."):
            try:
                prompt = f"Analiza como experto en Cancún: Precio ${precio}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta_usuario}"
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.error(f"La IA no pudo responder. Detalle: {e}")
    else:
        st.warning("Por favor, escribe una pregunta antes de hacer clic.")
