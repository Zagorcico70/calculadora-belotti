import streamlit as st
import requests
import time

st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- INTERFAZ ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Strategic Analysis - Cancún")

col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio Propiedad (USD)", value=1150000.0)
    renta = st.number_input("Renta Mensual (USD)", value=19050.0)
with col2:
    gastos = st.number_input("Gastos Mensuales (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación %", 0, 100, 85)

utilidad = ((renta * 12) * (ocupacion / 100)) - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0
st.metric("CAP RATE (ROI)", f"{cap_rate:.2f}%")

st.divider()
pregunta = st.text_input("Consultoría Estratégica AI:", placeholder="Ej: Análisis de plusvalía por Puente Nichupté")

if st.button("Generar Análisis Profesional"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("Configura la API Key.")
    else:
        # LISTA DE MODELOS POR PRIORIDAD
        # Si el 1.5 está lleno, saltamos al Pro, luego al 1.0.
        modelos_prioridad = [
            "gemini-1.5-flash", 
            "gemini-1.5-flash-8b", 
            "gemini-pro"
        ]
        
        analisis_completado = False
        
        with st.spinner("Belotti AI analizando datos de mercado..."):
            for modelo in modelos_prioridad:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
                payload = {
                    "contents": [{"parts": [{"text": f"Eres experto inmobiliario en Cancún. El ROI es {cap_rate:.2f}%. Pregunta: {pregunta}. Responde con autoridad profesional."}]}]
                }
                
                try:
                    res = requests.post(url, json=payload, timeout=10)
                    if res.status_code == 200:
                        texto = res.json()['candidates'][0]['content']['parts'][0]['text']
                        st.success(f"**Análisis Estratégico (Powered by {modelo}):**")
                        st.write(texto)
                        analisis_completado = True
                        break # Salimos del bucle si funciona
                    elif res.status_code == 503:
                        continue # Si está saturado, intenta el siguiente modelo
                except:
                    continue
            
            if not analisis_completado:
                st.error("Los servidores de Google están bajo mantenimiento global. Por favor, intenta en 30 segundos.")

st.sidebar.info("Asistente activo 24/7 con respaldo automático de modelos.")
