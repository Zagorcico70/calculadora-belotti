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

# --- SECCIÓN DE IA ---
st.divider()
pregunta = st.text_input("Pregunta a la IA sobre la inversión:")

if st.button("Analizar con Belotti AI"):
    # Esta línea busca la clave con cualquier nombre común que le hayas puesto
    api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("api_key")
    
    if not api_key:
        st.error("⚠️ La App no encuentra ninguna clave en 'Secrets'. Revisa el nombre en la configuración de Streamlit.")
    else:
        # URL directa que funciona con claves nuevas
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        contexto = (
            f"Eres un experto en Real Estate en Cancún. La propiedad cuesta ${precio:,.2f} USD "
            f"y tiene un Cap Rate de {cap_rate:.2f}%. Considera que el Puente Nichupté "
            f"se inauguró este domingo 3 de mayo de 2026. Responde a: {pregunta}"
        )
        
        payload = {
            "contents": [{"parts": [{"text": contexto}]}]
        }
        
        with st.spinner("Conectando con el cerebro de la IA..."):
            try:
                res = requests.post(url, json=payload, timeout=15)
                if res.status_code == 200:
                    respuesta_texto = res.json()['candidates'][0]['content']['parts'][0]['text']
                    st.info(respuesta_texto)
                else:
                    # Esto nos dirá exactamente qué dice Google si rechaza la clave
                    st.error(f"Google dice: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"Error de red: {e}")
