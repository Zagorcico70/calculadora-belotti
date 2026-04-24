import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- INTERFAZ ---
st.title("📊 Belotti Analytics")
col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio Venta (USD)", value=1150000.0)
    renta = st.number_input("Renta Mensual (USD)", value=19050.0)
with col2:
    gastos = st.number_input("Gastos Mensuales (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación %", 0, 100, 70)

utilidad = (renta * 12 * (ocupacion/100)) - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Ingreso Anual", f"${(renta * 12 * (ocupacion/100)):,.2f}")
m2.metric("Utilidad Neta", f"${utilidad:,.2f}")
m3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONSULTORÍA IA (CONEXIÓN MANUAL) ---
st.divider()
st.subheader("🤖 Consultoría IA Belotti")
pregunta = st.text_input("¿Qué quieres analizar?")

if st.button("Analizar con IA"):
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        # URL Directa de Google (Saltamos la librería)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": f"Eres experto inmobiliario en Cancún. Analiza estos datos: Precio ${precio}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"}]
            }]
        }
        
        with st.spinner("Analizando..."):
            try:
                response = requests.post(url, headers=headers, json=payload)
                data = response.json()
                # Extraemos la respuesta del JSON de Google
                texto_ia = data['candidates'][0]['content']['parts'][0]['text']
                st.info(texto_ia)
            except Exception as e:
                st.error("Error en la conexión manual. Verifica tu API Key.")
                st.write(f"Detalle técnico: {data if 'data' in locals() else e}")
    else:
        st.error("No se encontró la API Key en Secrets.")
