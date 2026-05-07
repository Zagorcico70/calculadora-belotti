import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

st.title("📊 Belotti Analytics")
st.subheader("Real Estate Strategy - Cancún")

# --- CALCULADORA ---
precio = st.number_input("Precio Propiedad (USD)", value=1150000.0)
renta = st.number_input("Renta Mensual (USD)", value=19050.0)
cap_rate = ((renta * 12) / precio) * 100 if precio > 0 else 0
st.metric("ROI / CAP RATE", f"{cap_rate:.2f}%")

# --- IA PROFESIONAL ---
st.divider()
pregunta = st.text_input("Haz tu pregunta al asistente:")

if st.button("Ejecutar Análisis"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Configura la clave en Secrets.")
    else:
        # Probamos la ruta 'v1' que es la que exigen las cuentas con facturación activa
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Eres experto inmobiliario en Cancún. El ROI es {cap_rate:.2f}%. Pregunta: {pregunta}"
                }]
            }]
        }
        
        with st.spinner("Conectando con el servidor de alta prioridad..."):
            try:
                response = requests.post(url, json=payload, timeout=20)
                
                if response.status_code == 200:
                    res_json = response.json()
                    st.success(res_json['candidates'][0]['content']['parts'][0]['text'])
                else:
                    # Si falla la v1, intentamos la v1beta como respaldo
                    url_beta = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    response_beta = requests.post(url_beta, json=payload, timeout=20)
                    
                    if response_beta.status_code == 200:
                        st.success(response_beta.json()['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Error de Google ({response_beta.status_code}): {response_beta.text}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
