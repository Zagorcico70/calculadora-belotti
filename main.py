import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- CALCULADORA ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment - Cancún")

precio = st.number_input("Precio (USD)", value=1150000.0)
renta = st.number_input("Renta Mensual (USD)", value=19050.0)
gastos = st.number_input("Gastos Mensuales (USD)", value=1000.0)
ocupacion = st.slider("Ocupación %", 0, 100, 85)

# Cálculos
utilidad = ((renta * 12) * (ocupacion / 100)) - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONEXIÓN IA ---
st.divider()
pregunta = st.text_input("Pregunta a la IA:")

if st.button("Analizar"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Configura GEMINI_API_KEY en los Secrets.")
    else:
        # RUTA V1BETA: La única que funciona para modelos Flash en proyectos nuevos
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Eres experto en Real Estate en Cancún. El ROI es {cap_rate:.2f}%. Responde: {pregunta}"
                }]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        
        with st.spinner("Analizando..."):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=15)
                
                if response.status_code == 200:
                    respuesta = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success(respuesta)
                else:
                    # Si falla Flash, intentamos con Gemini Pro (Ruta antigua)
                    url_pro = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                    response_pro = requests.post(url_pro, headers=headers, json=payload, timeout=15)
                    
                    if response_pro.status_code == 200:
                        respuesta_pro = response_pro.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(respuesta_pro)
                    else:
                        st.error(f"Error de Google: {response_pro.status_code}. Mensaje: {response_pro.text}")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
