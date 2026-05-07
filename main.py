import streamlit as st
import requests

# Configuración de página
st.set_page_config(page_title="Belotti Analytics", page_icon="📊", layout="wide")

# --- CALCULADORA DE INVERSIÓN ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment Audit - Cancún")

col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio de Venta (USD)", value=1150000.0)
    renta = st.number_input("Renta Mensual Bruta (USD)", value=19050.0)
with col2:
    gastos = st.number_input("Gastos Mensuales (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación Anual %", 0, 100, 85)

# Cálculos financieros
ingreso_anual = (renta * 12) * (ocupacion / 100)
utilidad = ingreso_anual - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Ingreso Anual", f"${ingreso_anual:,.0f}")
m2.metric("Utilidad Neta", f"${utilidad:,.0f}")
m3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONSULTORÍA CON IA (GEMINI) ---
st.divider()
st.subheader("🤖 Belotti AI Strategic Consultant")
pregunta = st.text_input("Haz tu pregunta sobre la inversión:", placeholder="Ej: ¿Cómo impacta el Puente Nichupté?")

if st.button("Ejecutar Análisis"):
    if pregunta:
        # Buscamos la clave en los Secrets
        api_key = st.secrets.get("GEMINI_API_KEY") or st.secrets.get("GOOGLE_API_KEY")
        
        if not api_key:
            st.error("⚠️ Error: No se encontró la API Key en los Secrets de Streamlit.")
        else:
            # URL ESTABLE V1 - Esta es la que Google recomienda para evitar el 404
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            headers = {'Content-Type': 'application/json'}
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": (
                            f"Actúa como un experto en Real Estate de Cancún. "
                            f"Contexto: Propiedad de ${precio:,.0f} USD con un ROI (Cap Rate) de {cap_rate:.2f}%. "
                            f"Inauguración del Puente Nichupté: 3 de mayo de 2026. "
                            f"Pregunta: {pregunta}. RESPONDE EN EL IDIOMA DEL USUARIO."
                        )
                    }]
                }]
            }
            
            with st.spinner("Analizando mercado con IA..."):
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=20)
                    
                    if response.status_code == 200:
                        res_json = response.json()
                        # Extraer respuesta correctamente
                        respuesta_ia = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.info(respuesta_ia)
                    elif response.status_code == 404:
                        st.error("Error 404: El modelo aún no está disponible para esta clave. Intenta de nuevo en un momento o verifica la activación en Google Cloud.")
                    else:
                        st.error(f"Error {response.status_code}: {response.text}")
                        
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
    else:
        st.warning("Por favor, escribe una pregunta primero.")

# Pie de página
st.sidebar.write("Belotti Analytics | Cancún 2026")
