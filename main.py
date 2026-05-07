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

st.divider()
pregunta = st.text_input("Haz tu pregunta al asistente:")

if st.button("Ejecutar Análisis"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Configura la clave en Secrets.")
    else:
        # Esta es la URL que acepta API KEY y usa tu facturación de Google Cloud
        # Usamos la v1 (versión estable de producción)
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Eres experto inmobiliario en Cancún. El ROI es {cap_rate:.2f}%. Pregunta: {pregunta}"
                }]
            }]
        }
        
        with st.spinner("Analizando con prioridad alta..."):
            try:
                response = requests.post(url, json=payload, timeout=20)
                
                if response.status_code == 200:
                    res_json = response.json()
                    st.success("**Análisis Estratégico:**")
                    st.write(res_json['candidates'][0]['content']['parts'][0]['text'])
                elif response.status_code == 404:
                    # Si la v1 falla, intentamos v1beta (a veces los proyectos nuevos están aquí)
                    url_beta = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    res_beta = requests.post(url_beta, json=payload, timeout=20)
                    if res_beta.status_code == 200:
                        st.success(res_beta.json()['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Error {res_beta.status_code}: Revisa si la API de Gemini está habilitada en Google Cloud.")
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error(f"Error de conexión: {e}")
