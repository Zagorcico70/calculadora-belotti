import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

st.title("📊 Belotti Analytics")
st.subheader("Estrategia Inmobiliaria - Cancún")

# --- CALCULADORA ---
precio = st.number_input("Precio Propiedad (USD)", value=1150000.0)
renta = st.number_input("Renta Mensual (USD)", value=19050.0)
cap_rate = ((renta * 12) / precio) * 100 if precio > 0 else 0
st.metric("ROI / CAP RATE", f"{cap_rate:.2f}%")

st.divider()

if st.button("ANALIZAR INVERSIÓN"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Falta la clave en Secrets.")
    else:
        # CAMBIO CLAVE: Usamos 'v1' y el nombre completo del modelo
        # Esta es la ruta exacta para cuentas con Google Cloud Billing
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Eres experto inmobiliario en Cancún. El ROI es {cap_rate:.2f}%. Dame un consejo breve."
                }]
            }]
        }
        
        with st.spinner("Conectando con el modelo de producción..."):
            try:
                response = requests.post(url, json=payload, timeout=15)
                
                if response.status_code == 200:
                    st.balloons()
                    st.success("**¡CONEXIÓN EXITOSA!**")
                    st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    # Si falla, te diré qué otros modelos tienes disponibles
                    st.error(f"Error {response.status_code}")
                    st.write("Respuesta de Google:", response.json())
            except Exception as e:
                st.error(f"Error de conexión: {e}")
