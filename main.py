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

utilidad = ((renta * 12) * (ocupacion / 100)) - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0
st.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- IA AUTO-CONFIGURABLE ---
st.divider()
pregunta = st.text_input("Pregunta a la IA:")

if st.button("Analizar"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("Falta la clave en Secrets.")
    else:
        with st.spinner("Buscando modelo disponible en tu cuenta..."):
            try:
                # 1. PASO DE DIAGNÓSTICO: Listamos los modelos que TÚ tienes habilitados
                list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
                list_res = requests.get(list_url)
                
                if list_res.status_code == 200:
                    modelos = list_res.json().get('models', [])
                    # Buscamos uno que permita generar contenido (Flash o Pro)
                    modelo_a_usar = next((m['name'] for m in modelos if 'generateContent' in m['supportedGenerationMethods']), None)
                    
                    if modelo_a_usar:
                        # 2. USAMOS EL MODELO ENCONTRADO
                        gen_url = f"https://generativelanguage.googleapis.com/v1beta/{modelo_a_usar}:generateContent?key={api_key}"
                        payload = {"contents": [{"parts": [{"text": f"Experto en Cancún. ROI: {cap_rate:.2f}%. Pregunta: {pregunta}"}]}]}
                        
                        gen_res = requests.post(gen_url, json=payload)
                        if gen_res.status_code == 200:
                            st.success(gen_res.json()['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error(f"Error al generar: {gen_res.text}")
                    else:
                        st.error("Tu clave no tiene ningún modelo de generación habilitado. Revisa Google AI Studio.")
                else:
                    st.error(f"No se pudo listar modelos: {list_res.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")
