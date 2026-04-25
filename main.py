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

# --- CONSULTORÍA CON GROQ (IA) ---
st.divider()
st.subheader("🤖 Belotti AI Consulting")
pregunta = st.text_input("Haz una pregunta técnica sobre este ROI:", placeholder="Ej: ¿Cómo optimizar este Cap Rate?")

if st.button("Analizar con IA"):
    if pregunta:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Usamos el modelo Llama 3.3 70b (El más potente y actual en Groq)
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Eres un experto asesor inmobiliario certificado en Cancún. Analizas inversiones con ética y precisión técnica."
                    },
                    {
                        "role": "user", 
                        "content": f"Inversión: ${precio} USD, Cap Rate: {cap_rate:.2f}%. Pregunta: {pregunta}"
                    }
                ],
                "temperature": 0.7
            }
            
            with st.spinner("Analizando con Groq..."):
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=15)
                    if response.status_code == 200:
                        respuesta = response.json()['choices'][0]['message']['content']
                        st.info(respuesta)
                    else:
                        error_msg = response.json().get('error', {}).get('message', 'Error desconocido')
                        st.error(f"Error de Groq: {error_msg}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
        else:
            st.error("⚠️ Configura 'GROQ_API_KEY' en los Secrets de Streamlit.")
    else:
        st.warning("Escribe una pregunta para el consultor.")
