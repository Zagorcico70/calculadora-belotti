import streamlit as st
import requests

st.set_page_config(page_title="Belotti Analytics AI", page_icon="📊", layout="wide")

# --- BARRA LATERAL (HÍBRIDA) ---
st.sidebar.header("⚙️ Configuración del Análisis")

# Selector de modo para no perder tu funcionalidad original
modo_analisis = st.sidebar.radio(
    "Selecciona el tipo de producto:",
    ("Inversión de Flujo (ROI)", "Adquisición Patrimonial (Branded)")
)

st.sidebar.divider()

# Variables iniciales
propiedad_input = ""
precio = 0.0
cap_rate = 0.0

if modo_analisis == "Inversión de Flujo (ROI)":
    st.sidebar.subheader("📊 Datos de Inversión")
    propiedad_input = st.sidebar.text_input("Ubicación o Nombre del Proyecto:")
    precio = st.sidebar.number_input("Precio Propiedad (USD)", value=0.0, step=10000.0)
    renta = st.sidebar.number_input("Renta Mensual Estimada (USD)", value=0.0, step=500.0)
    mantenimiento = st.sidebar.number_input("Mantenimiento Mensual (USD)", value=0.0, step=100.0)
    
    ingreso_anual = (renta - mantenimiento) * 12
    cap_rate = (ingreso_anual / precio) * 100 if precio > 0 else 0
    st.sidebar.metric("ROI NETO", f"{cap_rate:.2f}%")

else:  # Modo Adquisición Patrimonial
    st.sidebar.subheader("🏢 Datos de Marca (Branded)")
    propiedad_input = st.sidebar.text_input("Proyecto (ej. Thompson, SLS):")
    precio = st.sidebar.number_input("Precio Venta (USD)", value=0.0, step=10000.0)
    factor_marca = st.sidebar.slider("Premium de Marca (Factor):", 1.0, 1.4, 1.25, 0.01)
    
    valor_patrimonial = precio * factor_marca
    st.sidebar.metric("VALOR PATRIMONIAL", f"${valor_patrimonial:,.0f}")
    st.sidebar.caption("Basado en factor de plusvalía de marca.")

idioma = st.sidebar.selectbox("Idioma de respuesta:", ["Español", "English", "Italiano"])

# --- CUERPO PRINCIPAL ---
if modo_analisis == "Inversión de Flujo (ROI)":
    st.title("📊 Belotti Analytics: ROI & Cashflow")
else:
    st.title("💎 Belotti Analytics: Strategic Branding")

if propiedad_input:
    st.info(f"Análisis Estratégico para: **{propiedad_input}**")
else:
    st.warning("👈 Ingresa los datos en la barra lateral para comenzar.")

if "historial" not in st.session_state:
    st.session_state.historial = []
if "ultimo_analisis" not in st.session_state:
    st.session_state.ultimo_analisis = ""

user_input = st.text_input("Haz una consulta o pide un análisis:")

col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    enviar = st.button("🚀 Enviar")
with col2:
    if st.button("🧹 Limpiar"):
        st.session_state.historial = []
        st.session_state.ultimo_analisis = ""
        st.rerun()

if enviar and user_input:
    api_key = st.secrets.get("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    contexto = f"""
    Eres Antonio Belotti, experto en Real Estate Data Analysis en Cancún. 
    Modo actual: {modo_analisis}.
    Propiedad: {propiedad_input}. Precio: {precio} USD.
    Instrucción: Responde en {idioma} de forma profesional. Sin LaTeX.
    """
    
    payload = {"contents": [{"parts": [{"text": f"{contexto}\nPregunta: {user_input}"}]}]}
    
    with st.spinner("Analizando..."):
        try:
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                respuesta = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.session_state.historial.append({"user": user_input, "ia": respuesta})
                st.session_state.ultimo_analisis = respuesta
            else:
                st.error("Error en la conexión.")
        except Exception as e:
            st.error(f"Error: {e}")

# --- SECCIÓN DE WHATSAPP ---
if st.session_state.ultimo_analisis:
    st.divider()
    if st.button("📱 GENERAR RESUMEN PARA WHATSAPP"):
        api_key = st.secrets.get("GEMINI_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        
        prompt_wa = f"""
        Basado en este análisis: "{st.session_state.ultimo_analisis}", 
        crea un resumen ejecutivo para enviar por WhatsApp a un cliente.
        Debe ser persuasivo, usar emojis. Incluye los datos clave del modo {modo_analisis}.
        Firma como Antonio Belotti. Idioma: {idioma}.
        """
        
        payload_wa = {"contents": [{"parts": [{"text": prompt_wa}]}]}
        
        with st.spinner("Preparando mensaje..."):
            res_wa = requests.post(url, json=prompt_wa)
            # Nota: Asegúrate de que tu llamada POST esté correctamente estructurada aquí como en tu código original
            res_wa = requests.post(url, json=payload_wa)
            if res_wa.status_code == 200:
                mensaje_wa = res_wa.json()['candidates'][0]['content']['parts'][0]['text']
                st.text_area("Copia y pega este mensaje en WhatsApp:", value=mensaje_wa, height=300)
                st.success("¡Mensaje listo para enviar!")

# Mostrar chat
for chat in reversed(st.session_state.historial):
    with st.chat_message("assistant", avatar="📊"):
        st.write(chat["ia"])
    with st.chat_message("user"):
        st.write(chat["user"])
