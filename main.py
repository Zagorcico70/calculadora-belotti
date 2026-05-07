import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics AI", page_icon="📊", layout="wide")

# --- BARRA LATERAL ---
st.sidebar.header("📊 Datos de la Inversión")

# AQUÍ: Ahora tú escribes la zona o propiedad que quieras
propiedad_input = st.sidebar.text_input("Ubicación o Nombre del Proyecto:", placeholder="Ej: Puerto Cancún, SM 15, Villa Magna...")

precio = st.sidebar.number_input("Precio Propiedad (USD)", value=0.0, step=10000.0)
renta = st.sidebar.number_input("Renta Mensual Estimada (USD)", value=0.0, step=500.0)
mantenimiento = st.sidebar.number_input("Mantenimiento Mensual (USD)", value=0.0, step=100.0)
idioma = st.sidebar.selectbox("Idioma de respuesta:", ["Español", "English", "Italiano"])

# Cálculo automático de ROI
ingreso_anual = (renta - mantenimiento) * 12
cap_rate = (ingreso_anual / precio) * 100 if precio > 0 else 0

st.sidebar.divider()
st.sidebar.metric("ROI NETO CALCULADO", f"{cap_rate:.2f}%")

# --- CUERPO PRINCIPAL ---
st.title("📊 Belotti Analytics")

# El título cambia según lo que escribas en la barra lateral
if propiedad_input:
    st.info(f"Análisis Estratégico para: **{propiedad_input}**")
else:
    st.warning("👈 Por favor, ingresa una ubicación en la barra lateral para comenzar.")

if "historial" not in st.session_state:
    st.session_state.historial = []

user_input = st.text_input("Escribe tu consulta para la IA (ej: ¿Cuál es el potencial de plusvalía aquí?):")

col1, col2 = st.columns([1, 5])
with col1:
    enviar = st.button("Enviar")
with col2:
    if st.button("Limpiar Chat"):
        st.session_state.historial = []
        st.rerun()

if enviar and user_input:
    api_key = st.secrets.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    # Contexto dinámico: La IA sabe exactamente qué propiedad estás analizando
    contexto = f"""
    Eres Antonio Belotti, experto en Real Estate Data Analysis en Cancún. 
    Propiedad/Zona: {propiedad_input if propiedad_input else 'Cancún (General)'}. 
    Precio: {precio} USD. ROI Neto: {cap_rate:.2f}%.
    Instrucción: Responde en {idioma} de forma profesional y comercial. No uses LaTeX ni símbolos $.
    """
    
    payload = {"contents": [{"parts": [{"text": f"{contexto}\nPregunta del cliente: {user_input}"}]}]}
    
    with st.spinner("Analizando mercado..."):
        try:
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                respuesta = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.session_state.historial.append({"user": user_input, "ia": respuesta})
            else:
                st.error("Error de conexión. Verifica tu API Key.")
        except Exception as e:
            st.error(f"Error: {e}")

# Mostrar el chat de forma elegante
for chat in reversed(st.session_state.historial):
    with st.chat_message("assistant", avatar="📊"):
        st.write(chat["ia"])
    with st.chat_message("user"):
        st.write(chat["user"])
