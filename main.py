import streamlit as st
import requests

# Configuración básica
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

# --- IA ---
st.divider()
pregunta = st.text_input("Pregunta a la IA sobre la inversión:")

if st.button("Analizar con Belotti AI"):
    # Buscamos la clave en los Secrets
    api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("⚠️ No se encontró la clave API en los Secrets de Streamlit.")
    else:
        # URL CORREGIDA: Versión v1 y modelo -latest para evitar el error 404
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Eres un experto en Real Estate en Cancún. La propiedad cuesta ${precio} USD con un Cap Rate de {cap_rate:.2f}%. Pregunta: {pregunta}"
                }]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        
        with st.spinner("Analizando..."):
            try:
                # Usamos la URL v1 que es la que Google recomienda ahora
                response = requests.post(url, headers=headers, json=payload, timeout=15)
                
                if response.status_code == 200:
                    res_json = response.json()
                    st.info(res_json['candidates'][0]['content']['parts'][0]['text'])
                else:
                    # Si falla v1, intentamos v1beta automáticamente en el mismo bloque
                    url_beta = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                    response_beta = requests.post(url_beta, headers=headers, json=payload, timeout=15)
                    
                    if response_beta.status_code == 200:
                        res_json_beta = response_beta.json()
                        st.info(res_json_beta['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"Error final de Google: {response_beta.status_code}. Por favor, verifica que tu API Key tenga habilitado 'Generative Language API' en el Google Cloud Console.")
            except Exception as e:
                st.error(f"Error de conexión: {e}")
