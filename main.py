import streamlit as st
import requests
import json

# Configuración de la página
st.set_page_config(page_title="Belotti Analytics", page_icon="📊", layout="wide")

# --- ESTILOS ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment Audit - Cancún")
st.write("Análisis de rentabilidad con impacto del Puente Nichupté.")

# --- CALCULADORA ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        precio = st.number_input("Precio de Venta (USD)", value=1150000.0)
        renta = st.number_input("Renta Mensual Bruta (USD)", value=19050.0)
    with col2:
        gastos = st.number_input("Gastos Mensuales (USD)", value=1000.0)
        ocupacion = st.slider("Ocupación Anual %", 0, 100, 85)

# Cálculos
ingreso_anual = (renta * 12) * (ocupacion / 100)
utilidad = ingreso_anual - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.divider()

# Métricas
m1, m2, m3 = st.columns(3)
m1.metric("Ingreso Anual", f"${ingreso_anual:,.0f}")
m2.metric("Utilidad Neta", f"${utilidad:,.0f}")
m3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONSULTORÍA CON IA ---
st.divider()
st.subheader("🤖 Belotti AI Consultant")
pregunta = st.text_input("Haz tu pregunta sobre la inversión:", placeholder="Ej: ¿Es sostenible este ROI con el nuevo puente?")

if st.button("Ejecutar Análisis"):
    if pregunta:
        # Priorizamos el nombre del secreto que tienes
        api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
        
        if api_key:
            # Lista de URLs para probar (evita el error 404 por versión)
            urls_to_try = [
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}",
                f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            ]
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"Eres un experto en Real Estate en Cancún. Contexto: Precio ${precio}, ROI {cap_rate:.2f}%. Pregunta: {pregunta}. Responde en el idioma del usuario."}]
                }]
            }
            
            success = False
            with st.spinner("Analizando..."):
                for url in urls_to_try:
                    try:
                        response = requests.post(url, json=payload, timeout=15)
                        if response.status_code == 200:
                            res_json = response.json()
                            respuesta_texto = res_json['candidates'][0]['content']['parts'][0]['text']
                            st.info(respuesta_texto)
                            success = True
                            break # Si funciona, salimos del bucle
                    except:
                        continue
                
                if not success:
                    st.error("Error: No se pudo conectar con la IA. Por favor, verifica que tu API Key sea válida en Google AI Studio.")
        else:
            st.error("⚠️ No se encontró la API Key en los Secrets de Streamlit.")
    else:
        st.warning("Escribe una pregunta.")
