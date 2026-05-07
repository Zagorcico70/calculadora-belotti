import streamlit as st
import requests
import time

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# Esto limpia la memoria interna de Streamlit cada vez que reinicias
st.cache_data.clear()

st.title("📊 Belotti Analytics")
st.subheader("Estrategia Inmobiliaria - Cancún")

# --- CALCULADORA ---
precio = st.number_input("Precio Propiedad (USD)", value=1150000.0)
renta = st.number_input("Renta Mensual (USD)", value=19050.0)
cap_rate = ((renta * 12) / precio) * 100 if precio > 0 else 0
st.metric("ROI / CAP RATE", f"{cap_rate:.2f}%")

st.divider()

if st.button("FORZAR CONEXIÓN IA"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ No hay clave en Secrets.")
    else:
        # Intentamos la URL más cruda y directa posible
        # A veces el 'v1beta' funciona cuando el 'v1' da 404 por falta de propagación
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Responde solo: 'Conexión exitosa, Antonio'. ROI actual: {cap_rate:.2f}%"
                }]
            }]
        }
        
        with st.spinner("Buscando señal en los servidores de Google..."):
            # Reintento automático: lo intenta 2 veces por si la primera falla por lag
            for intento in range(2):
                try:
                    response = requests.post(url, json=payload, timeout=15)
                    if response.status_code == 200:
                        st.balloons()
                        st.success("**¡POR FIN! CONECTADO:**")
                        st.write(response.json()['candidates'][0]['content']['parts'][0]['text'])
                        break
                    elif intento == 0:
                        time.sleep(2) # Espera 2 segundos y reintenta
                        continue
                    else:
                        st.error(f"Error {response.status_code}")
                        st.write("Google dice:", response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
