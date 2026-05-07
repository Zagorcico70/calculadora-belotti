import streamlit as st
import requests

# Configuración de la página
st.set_page_config(page_title="Belotti Analytics", page_icon="📊", layout="wide")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- ENCABEZADO ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment Audit - Cancún & Riviera Maya")
st.write(f"Análisis actualizado tras la inauguración del Puente Nichupté.")

# --- CALCULADORA DE INVERSIÓN ---
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 💰 Datos de la Propiedad")
        precio = st.number_input("Precio de Venta (USD)", value=1150000.0, step=1000.0)
        renta = st.number_input("Renta Mensual Bruta Estimada (USD)", value=19050.0, step=100.0)
    
    with col2:
        st.markdown("### ⚙️ Operación")
        gastos = st.number_input("Gastos Mensuales / Mantenimiento (USD)", value=1000.0, step=50.0)
        ocupacion = st.slider("Porcentaje de Ocupación Anual %", 0, 100, 85)

# Cálculos Financieros
ingreso_anual_bruto = (renta * 12) * (ocupacion / 100)
gastos_anuales = gastos * 12
utilidad_neta_anual = ingreso_anual_bruto - gastos_anuales
cap_rate = (utilidad_neta_anual / precio) * 100 if precio > 0 else 0

st.divider()

# --- MÉTRICAS PRINCIPALES ---
m1, m2, m3 = st.columns(3)
m1.metric("Ingreso Anual Bruto", f"${ingreso_anual_bruto:,.2f}")
m2.metric("Utilidad Neta Anual", f"${utilidad_neta_anual:,.2f}", delta_color="normal")
m3.metric("CAP RATE (ROI)", f"{cap_rate:.2f}%")

# --- CONSULTORÍA ESTRATÉGICA CON IA (GEMINI) ---
st.divider()
st.subheader("🤖 Belotti AI Strategic Consultant")
st.info("La IA analizará este Cap Rate considerando la ubicación en Cancún y el impacto del nuevo Puente Nichupté.")

pregunta = st.text_input(
    "Haz una pregunta técnica sobre esta inversión:",
    placeholder="Ej: ¿Cómo afecta el Puente Nichupté a la plusvalía de este edificio?"
)

if st.button("Ejecutar Análisis de IA"):
    if pregunta:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            
            # URL Directa v1 (La más estable)
            
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"
            
            headers = {'Content-Type': 'application/json'}
            
            # Construcción del Prompt con contexto de experto
            contexto = (
                f"Eres un asesor experto en Real Estate Data Analytics en Cancún. "
                f"El usuario está analizando una propiedad de ${precio:,.2f} USD con un Cap Rate de {cap_rate:.2f}%. "
                f"Considera que el Puente Nichupté se inauguró el 3 de mayo de 2026, mejorando la conectividad. "
                f"Responde de forma profesional y SIEMPRE en el idioma en que el usuario pregunte. "
                f"Pregunta del usuario: {pregunta}"
            )
            
            payload = {
                "contents": [{
                    "parts": [{"text": contexto}]
                }]
            }
            
            with st.spinner("Analizando datos del mercado..."):
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=20)
                    
                    if response.status_code == 200:
                        data = response.json()
                        # Extraer respuesta de la estructura de Google
                        if 'candidates' in data and len(data['candidates']) > 0:
                            respuesta_ia = data['candidates'][0]['content']['parts'][0]['text']
                            st.markdown("### 📋 Análisis del Consultor:")
                            st.write(respuesta_ia)
                        else:
                            st.error("La IA no devolvió resultados. Verifica tu cuota en Google Cloud.")
                    elif response.status_code == 404:
                        st.error("Error 404: No se encontró el modelo. Verifica que la URL sea correcta o que la API Key sea válida.")
                    else:
                        st.error(f"Error de API ({response.status_code}): {response.text}")
                        
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
        else:
            st.error("⚠️ Falta la clave 'GEMINI_API_KEY' en los Secrets de Streamlit.")
    else:
        st.warning("Por favor, ingresa una pregunta para iniciar el análisis.")

# --- PIE DE PÁGINA ---
st.sidebar.markdown("---")
st.sidebar.write("Powered by **Belotti Analytics**")
st.sidebar.write("Cancún, México | 2026")
