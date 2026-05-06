import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN DE SEGURIDAD Y IA ---
# Asegúrate de tener GEMINI_API_KEY en tus Secrets de Streamlit
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Falta la clave API de Gemini en los Secretos.")

# --- INTERFAZ DE LA CALCULADORA ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment Audit - Cancún")

# Inputs de la calculadora
col1, col2 = st.columns(2)
with col1:
    precio_venta = st.number_input("Precio Venta (USD)", min_value=0.0, value=1150000.0)
    renta_mensual = st.number_input("Renta Mensual Bruta (USD)", min_value=0.0, value=16192.50)

with col2:
    gastos = st.number_input("Gastos/Mantenimiento (USD)", min_value=0.0, value=1000.0)
    ocupacion = st.slider("Ocupación Anual %", 0, 100, 100)

# --- CÁLCULOS MATEMÁTICOS ---
ingreso_anual = (renta_mensual * 12) * (ocupacion / 100)
utilidad_neta = ingreso_anual - (gastos * 12)
cap_rate = (utilidad_neta / precio_venta) * 100 if precio_venta > 0 else 0

# Mostrar resultados
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Ingreso Anual Est.", f"${ingreso_anual:,.0f}")
c2.metric("Utilidad Neta", f"${utilidad_neta:,.0f}")
c3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- SECCIÓN DE INTELIGENCIA ARTIFICIAL (BELOTTI AI) ---
st.divider()
st.header("🤖 Belotti AI Consulting")
st.info("Pregunta al consultor (Ask in English, Spanish or Italian)")

# Inicializar historial de chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Lógica del Chat
if prompt := st.chat_input("¿Qué duda tienes sobre esta inversión?"):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Crear el contexto para que la IA sepa qué números está analizando
    # Aquí aplicamos tu perfil de Asesor Certificado por CONOCER
    contexto_inversion = f"""
    Eres Antonio Belotti, asesor inmobiliario certificado por CONOCER[cite: 1]. 
    Respondes de forma profesional y trilingüe[cite: 1]. 
    DATOS ACTUALES DE LA CALCULADORA:
    - Precio de la propiedad: ${precio_venta:,.2f} USD
    - Ingreso Anual Estimado: ${ingreso_anual:,.2f} USD
    - Utilidad Neta: ${utilidad_neta:,.2f} USD
    - CAP RATE calculado: {cap_rate:.2f}%
    
    Analiza estos datos basándote en el mercado de Cancún y la Riviera Maya. 
    Si el cliente pregunta, usa esta información para dar una recomendación experta.
    """

    with st.chat_message("assistant"):
        with st.spinner("Consultando catálogo y analizando ROI..."):
            # Enviamos el contexto + la personalidad + la pregunta
            full_prompt = f"{contexto_inversion}\n\nPregunta del cliente: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
    
    # Guardar respuesta de la IA
    st.session_state.messages.append({"role": "assistant", "content": response.text})
