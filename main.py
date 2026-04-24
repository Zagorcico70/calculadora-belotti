import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- CONEXIÓN DIRECTA ---
if "GEMINI_API_KEY" in st.secrets:
    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Esta es la forma más estable de llamar al modelo en versiones anteriores
        model = genai.GenerativeModel('gemini-pro')
    except Exception as e:
        st.error(f"Error de configuración: {e}")
else:
    st.error("⚠️ Configura la clave API en los Secrets de Streamlit.")
    st.stop()

# --- CALCULADORA ---
st.title("📊 Belotti Analytics")
col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio (USD)", value=1150000.0)
    renta = st.number_input("Renta Mensual (USD)", value=19050.0)
with col2:
    gastos = st.number_input("Gastos (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación %", 0, 100, 70)

utilidad = (renta * 12 * (ocupacion/100)) - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Ingreso Anual", f"${(renta * 12 * (ocupacion/100)):,.2f}")
c2.metric("Utilidad Neta", f"${utilidad:,.2f}")
c3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONSULTORÍA ---
st.markdown("---")
st.subheader("🤖 Belotti AI Consulting")
pregunta = st.text_input("Consulta técnica:")

if st.button("Analizar con IA"):
    if pregunta:
        with st.spinner("Generando..."):
            try:
                # Usamos el método de generación más simple
                prompt = f"Inversión Cancún. Precio ${precio}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                # Si esto falla, nos dará el error de red real
                st.error(f"Error de red: {e}")
    else:
        st.warning("Escribe una pregunta.")
