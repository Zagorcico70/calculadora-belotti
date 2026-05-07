import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics AI", page_icon="📊", layout="wide")

# --- BARRA LATERAL ---
st.sidebar.header("📊 Configuración de Inversión")
propiedad = st.sidebar.text_input("Nombre/Ubicación de la Propiedad:", value="Villas Marlin, Zona Hotelera")
precio = st.sidebar.number_input("Precio Propiedad (USD)", value=1150000.0)
renta = st.sidebar.number_input("Renta Mensual (USD)", value=19050.0)
mantenimiento = st.sidebar.number_input("Mantenimiento Mensual (USD)", value=500.0)
idioma = st.sidebar.selectbox("Idioma de respuesta:", ["Español", "English", "Italiano"])

ingreso_anual = (renta - mantenimiento) * 12
cap_rate = (ingreso_anual / precio) * 100 if precio > 0 else 0

st.sidebar.divider()
st.sidebar.metric("ROI NETO ESTIMADO", f"{cap_rate:.2f}%")

# --- CUERPO PRINCIPAL ---
st.title("📊 Belotti Analytics")
st.info(f"Asesorando sobre: **{propiedad}** | Motor: **Gemini 2.5 Flash**")

if "historial" not in st.session_state:
    st.session_state.historial = []

user_input = st.text_input("Haz una pregunta técnica o pide un argumento de venta:")

if st.button("Enviar Consulta") and user_input:
    api_key = st.secrets.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    contexto = f"""
    Eres Antonio Belotti, experto en Real Estate Data Analysis en Cancún. 
    Propiedad: {propiedad}. Precio: {precio} USD. ROI: {cap_rate:.2f}%.
    Instrucción: Responde en {idioma}. No uses LaTeX ni símbolos matemáticos complejos ($), usa texto simple y profesional.
    """
    
    payload = {"contents": [{"parts": [{"text": f"{contexto}\nPregunta: {user_input}"}]}]}
    
    with st.spinner("Analizando..."):
        try:
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                respuesta = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.session_state.historial.append({"user": user_input, "ia": respuesta})
            else:
                st.error("Error en la conexión con Google.")
        except Exception as e:
            st.error(f"Error: {e}")

for chat in reversed(st.session_state.historial):
    with st.chat_message("assistant", avatar="📊"):
        st.write(chat["ia"])
    with st.chat_message("user"):
        st.write(chat["user"])
