import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- CALCULADORA ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment - Cancún")

col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio (USD)", value=1150000.0)
    renta = st.number_input("Renta Mensual (USD)", value=19050.0)
with col2:
    gastos = st.number_input("Gastos Mensuales (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación %", 0, 100, 85)

# Cálculos rápidos
utilidad = ((renta * 12) * (ocupacion / 100)) - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0
st.metric("CAP RATE (ROI)", f"{cap_rate:.2f}%")

# --- SECCIÓN DE IA ---
st.divider()
pregunta = st.text_input("Pregunta a la IA sobre esta inversión:")

if st.button("Analizar con Belotti AI"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ No hay clave en Secrets. Pon la que empieza con 'AIza...'")
    else:
        # ESTA URL ES LA QUE GOOGLE ASIGNA POR DEFECTO A PROYECTOS "GEN-LANG-CLIENT"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Actúa como experto inmobiliario en Cancún. La propiedad tiene un ROI del {cap_rate:.2f}%. Responde: {pregunta}"
                }]
            }]
        }
        
        with st.spinner("Conectando..."):
            try:
                response = requests.post(url, json=payload, timeout=15)
                if response.status_code == 200:
                    try:
                        # Extraemos el texto de la respuesta
                        texto_ia = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(texto_ia)
                    except:
                        st.error("Google respondió pero el formato es inesperado.")
                elif response.status_code == 404:
                    st.error("Error 404: Google todavía no reconoce el modelo en tu cuenta. Espera 2 minutos o activa 'Generative Language API' en tu consola de Google Cloud.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
