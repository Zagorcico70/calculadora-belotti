import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- CALCULADORA ---
st.title("📊 Belotti Analytics")
col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio Venta (USD)", value=1150000.0)
    renta = st.number_input("Renta Mensual (USD)", value=19050.0)
with col2:
    gastos = st.number_input("Gastos Mensuales (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación %", 0, 100, 85)

utilidad = (renta * 12 * (ocupacion/100)) - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Utilidad Anual", f"${utilidad:,.0f}")
m3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONSULTORÍA IA ---
st.divider()
st.subheader("🤖 Belotti AI Consulting")
pregunta = st.text_input("Pregunta al consultor:")

if st.button("Analizar con IA"):
    if pregunta and "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        # USAMOS EL MODELO 8B: Es el que tiene menos restricciones de cuota
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-8b:generateContent?key={api_key}"
        
        payload = {
            "contents": [{"parts": [{"text": f"Analiza como experto inmobiliario en Cancún: Precio ${precio}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"}]}]
        }
        
        with st.spinner("Analizando..."):
            try:
                response = requests.post(url, json=payload)
                data = response.json()
                if response.status_code == 200:
                    st.info(data['candidates'][0]['content']['parts'][0]['text'])
                else:
                    # Si falla, intentamos con el último recurso: Gemini 1.0 Pro
                    st.warning("El modelo 8B falló. Intentando conexión de respaldo...")
                    url_pro = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
                    response_pro = requests.post(url_pro, json=payload)
                    st.info(response_pro.json()['candidates'][0]['content']['parts'][0]['text'])
            except:
                st.error("Google sigue bloqueando la cuota. El problema es la configuración de tu cuenta de Google Cloud.")
    else:
        st.warning("Escribe una pregunta.")
