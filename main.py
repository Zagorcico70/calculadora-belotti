import streamlit as st
import requests

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

# --- CONSULTORÍA CON GEMINI (CONEXIÓN DIRECTA) ---
st.divider()
st.subheader("🤖 Belotti AI Consulting")
pregunta = st.text_input("Pregunta al consultor (Ask in English or Spanish):", placeholder="Ej: What is the ROI outlook for this zone?")

if st.button("Analizar con IA"):
    if pregunta:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            headers = {'Content-Type': 'application/json'}
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"You are a certified Real Estate expert in Cancun. Respond in the user's language. Context: Price ${precio}, Cap Rate {cap_rate:.2f}%. Question: {pregunta}"
                    }]
                }]
            }
            
            with st.spinner("Analizando..."):
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=20)
                    if response.status_code == 200:
                        respuesta = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.info(respuesta)
                    else:
                        st.error(f"Error de API: {response.status_code}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
        else:
            st.error("⚠️ Configura 'GEMINI_API_KEY' en los Secrets.")
