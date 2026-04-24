import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE IA (Versión Robusta) ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Intentamos cargar el modelo de forma explícita
    # Si falla flash, intentamos con pro automáticamente
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
    except:
        model = genai.GenerativeModel('gemini-pro')
        
except Exception as e:
    st.error("Error al configurar la IA.")
    st.stop()

# ... (El resto de tu calculadora sigue igual) ...

# --- CAMBIO EN EL BOTÓN (Para ver el error real si persiste) ---
if st.button("Analizar con IA"):
    if pregunta:
        with st.spinner("Analizando..."):
            try:
                # Usamos una forma de envío de contenido más simple
                response = model.generate_content(
                    contents=f"Analiza como experto inmobiliario: Precio ${precio}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"
                )
                st.info(response.text)
            except Exception as e:
                # Esto nos dirá si es la llave, el modelo o la cuota
                st.error(f"Error específico: {e}")
