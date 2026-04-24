import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ROBUSTA ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Esta línea selecciona el modelo más estable del mercado
    model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
    
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# ... (Tu código de calculadora sigue igual debajo) ...

# --- CAMBIO EN EL BOTÓN DE ANÁLISIS ---
if st.button("Analizar con IA"):
    if pregunta:
        with st.spinner("Analizando..."):
            try:
                # Cambiamos 'contexto' por 'prompt' para mayor claridad
                prompt = f"Como experto inmobiliario en Cancún, analiza: Precio ${precio}, Renta Mensual ${renta_mensual}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                st.error("La IA está ocupada. Intenta de nuevo en unos segundos.")
                # Esto nos dirá el error real sin rodeos
                st.write(f"Detalle técnico: {e}")
