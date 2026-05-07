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
pregunta = st.text_input("Haz tu pregunta al asistente:", value="¿Es este un buen ROI para Cancún?")

if st.button("ANALIZAR AHORA"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ No hay clave API en los Secrets de Streamlit.")
    else:
        # LISTA DE PUERTAS (RUTAS) A PROBAR
        # La versión 'v1' es la que suelen exigir las cuentas con facturación activa
        rutas = [
            "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent",
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
            "https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent"
        ]
        
        exito = False
        with st.spinner("Probando rutas de alta prioridad..."):
            for url_base in rutas:
                url_completa = f"{url_base}?key={api_key}"
                payload = {
                    "contents": [{
                        "parts": [{
                            "text": f"Eres experto inmobiliario en Cancún. El ROI es {cap_rate:.2f}%. Pregunta: {pregunta}"
                        }]
                    }]
                }
                
                try:
                    response = requests.post(url_completa, json=payload, timeout=10)
                    if response.status_code == 200:
                        res_json = response.json()
                        st.success("**¡CONEXIÓN EXITOSA!**")
                        st.write(res_json['candidates'][0]['content']['parts'][0]['text'])
                        exito = True
                        break # Si funciona una, paramos de buscar
                except:
                    continue
            
            if not exito:
                st.error("Error 404 persistente: Google aún no propaga tu permiso.")
                st.info("Tony, intenta esto: En el panel de Streamlit Cloud, dale a 'Reboot App'. A veces el servidor de Streamlit guarda el error viejo y no intenta la conexión nueva.")
