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

if st.button("BUSCAR MODELO Y ANALIZAR"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ No hay clave en Secrets.")
    else:
        # PASO 1: Listar modelos disponibles para TU llave
        url_lista = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        
        try:
            with st.spinner("Consultando modelos autorizados para Belotti Analytics..."):
                res_lista = requests.get(url_lista)
                if res_lista.status_code == 200:
                    modelos_data = res_lista.json()
                    
                    # Buscamos el mejor modelo disponible que soporte generación de contenido
                    # Priorizamos 'gemini-1.5-flash' o 'gemini-pro'
                    modelos_validos = [m['name'] for m in modelos_data['models'] if "generateContent" in m['supportedGenerationMethods']]
                    
                    if not modelos_validos:
                        st.error("No se encontraron modelos de generación de contenido activos.")
                    else:
                        # Seleccionamos el mejor modelo disponible
                        modelo_a_usar = modelos_validos[0]
                        st.info(f"Conectando a: {modelo_a_usar}")
                        
                        # PASO 2: Hacer la consulta real
                        url_ai = f"https://generativelanguage.googleapis.com/v1beta/{modelo_a_usar}:generateContent?key={api_key}"
                        payload = {
                            "contents": [{
                                "parts": [{
                                    "text": f"Eres experto en Cancún. El ROI es {cap_rate:.2f}%. Dame un consejo breve sobre esta inversión."
                                }]
                            }]
                        }
                        
                        res_ai = requests.post(url_ai, json=payload)
                        if res_ai.status_code == 200:
                            st.balloons()
                            st.success("**¡ANÁLISIS EXITOSO!**")
                            st.write(res_ai.json()['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error(f"Error al generar: {res_ai.text}")
                else:
                    st.error("Google no reconoce tu API Key.")
                    st.write(res_lista.text)
        except Exception as e:
            st.error(f"Error de conexión: {e}")
