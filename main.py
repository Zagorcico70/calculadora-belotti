import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- INTERFAZ ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Strategic Analysis - Cancún")

precio = st.number_input("Precio Propiedad (USD)", value=1150000.0)
renta = st.number_input("Renta Mensual (USD)", value=19050.0)
gastos = st.number_input("Gastos Mensuales (USD)", value=1000.0)
ocupacion = st.slider("Ocupación %", 0, 100, 85)

utilidad = ((renta * 12) * (ocupacion / 100)) - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONEXIÓN IA ---
st.divider()
pregunta = st.text_input("Pregunta a la IA (Ej: Análisis de plusvalía):")

if st.button("Analizar"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ No se encontró la clave en los Secrets de Streamlit.")
    else:
        # Usamos la ruta estándar v1 que ahora ya debe estar activa
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Eres experto inmobiliario en Cancún. El ROI es {cap_rate:.2f}%. Responde a: {pregunta}"}]}]
        }
        
        with st.spinner("Consultando con la IA habilitada..."):
            try:
                response = requests.post(url, json=payload, timeout=15)
                if response.status_code == 200:
                    st.success(response.json()['candidates'][0]['content']['parts'][0]['text'])
                else:
                    # Si aún sale 404, Google tarda unos minutos en propagar la habilitación
                    st.error(f"Respuesta de Google ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
