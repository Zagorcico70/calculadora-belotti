import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics AI", page_icon="📊", layout="wide")

# Estilo personalizado para que se vea profesional
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007BFF; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Belotti Analytics: Inteligencia de Inversión")
st.sidebar.header("Configuración de Propiedad")

# --- SIDEBAR: DATOS TÉCNICOS ---
precio = st.sidebar.number_input("Precio Propiedad (USD)", value=1150000.0)
renta = st.sidebar.number_input("Renta Mensual (USD)", value=19050.0)
mantenimiento = st.sidebar.number_input("Mantenimiento Mensual (USD)", value=500.0)

# Cálculo de ROI Real (Neto aproximado)
ingreso_anual = (renta - mantenimiento) * 12
cap_rate = (ingreso_anual / precio) * 100 if precio > 0 else 0

st.sidebar.divider()
st.sidebar.metric("ROI NETO ESTIMADO", f"{cap_rate:.2f}%")

# --- CUERPO PRINCIPAL: CHAT CON LA IA ---
st.subheader("🤖 Consultoría Estratégica Belotti AI")
st.info(f"Conectado exitosamente al motor: **Gemini 2.5 Flash**")

# Historial de conversación sencillo
if "historial" not in st.session_state:
    st.session_state.historial = []

# Input de usuario
user_input = st.text_input("Escribe tu pregunta sobre la inversión (ej: ¿Cómo afecta el Tren Maya a esta zona?):")

col1, col2 = st.columns([1, 4])
with col1:
    boton_preguntar = st.button("Enviar Pregunta")
with col2:
    if st.button("Limpiar Chat"):
        st.session_state.historial = []
        st.rerun()

if boton_preguntar and user_input:
    api_key = st.secrets.get("GEMINI_API_KEY")
    
    if not api_key:
        st.error("Error: Configura la API Key en los Secrets.")
    else:
        # Usamos la ruta que ya confirmamos que te funciona: 2.5 Flash
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        contexto = f"""
        Eres Antonio Belotti, experto en Real Estate Data Analysis en Cancún. 
        Datos de la propiedad actual: Precio {precio} USD, ROI {cap_rate:.2f}%.
        Responde como un asesor experto, con visión de negocio y análisis de datos.
        """
        
        payload = {
            "contents": [{
                "parts": [{"text": f"{contexto}\nUsuario pregunta: {user_input}"}]
            }]
        }
        
        with st.spinner("Analizando mercado..."):
            try:
                res = requests.post(url, json=payload, timeout=20)
                if res.status_code == 200:
                    respuesta_ia = res.json()['candidates'][0]['content']['parts'][0]['text']
                    # Guardar en historial
                    st.session_state.historial.append({"user": user_input, "ia": respuesta_ia})
                else:
                    st.error(f"Error de conexión: {res.text}")
            except Exception as e:
                st.error(f"Error: {e}")

# Mostrar el chat
for chat in reversed(st.session_state.historial):
    with st.chat_message("user"):
        st.write(chat["user"])
    with st.chat_message("assistant", avatar="📊"):
        st.write(chat["ia"])
