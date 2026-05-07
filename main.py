import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- CALCULADORA ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment Audit - Cancún")

col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio Venta (USD)", value=1150000.0)
    renta = st.number_input("Renta Mensual Bruta (USD)", value=19050.0)
with col2:
    gastos = st.number_input("Gastos/Mantenimiento (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación Anual %", 0, 100, 85)

# Cálculos de rentabilidad
ingreso_anual = (renta * 12) * (ocupacion / 100)
utilidad = ingreso_anual - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Ingreso Anual Est.", f"${ingreso_anual:,.0f}")
m2.metric("Utilidad Neta", f"${utilidad:,.0f}")
m3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONSULTORÍA CON GEMINI (IA) ---
st.divider()
st.subheader("🤖 Belotti AI Consulting")
pregunta = st.text_input("Pregunta al consultor (Ask in English or Spanish):", placeholder="Ej: What is the ROI outlook for this zone?")

if st.button("Analizar con IA"):
    if pregunta:
        # Buscamos la clave de Google en los Secrets
        if "GOOGLE_API_KEY" in st.secrets:
            try:
                # Configuración de Gemini
                genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Contexto para el modelo
                prompt_sistema = (
                    "You are a certified Real Estate expert in Cancun. "
                    "MANDATORY: Respond ONLY in the same language the user uses. "
                    f"Context: Property Price ${precio} USD, Cap Rate {cap_rate:.2f}%. "
                    f"Question: {pregunta}"
                )

                with st.spinner("Analizando con Gemini..."):
                    response = model.generate_content(prompt_sistema)
                    st.info(response.text)
                    
            except Exception as e:
                st.error(f"Error técnico con Gemini: {e}")
        else:
            st.error("⚠️ Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    else:
        st.warning("Por favor, escribe una pregunta primero.")
