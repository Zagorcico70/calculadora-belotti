import streamlit as st
import requests
import google.generativeai as genai
import streamlit as st

# Configurar la llave que guardaste en secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Configurar el modelo y tu personalidad profesional
model = genai.GenerativeModel('gemini-1.5-flash', 
    system_instruction="""
    Eres Antonio Belotti, asesor inmobiliario certificado por CONOCER en la Riviera Maya. 
    Eres un experto trilingüe (Español, Italiano, Inglés) y especialista en análisis de datos.
    Tu objetivo es ayudar a inversionistas a entender el ROI y la plusvalía en Cancún y Bacalar.
    Utilizas los datos del 'catalogo_inversiones_cancun' para dar recomendaciones reales.
    """)
st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

# --- CALCULADORA ---
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment Audit - Cancún")

col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio Venta (USD)", value=1150000.0)
    renta = st.number_input("Renta Mensual Bruta (USD)", value=19050.0)
with col2:
    gastos = st.number_input("Gastos/Mantenimiento (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación Anual %", 0, 100, 85)

# Cálculos de rentabilidad
ingreso_anual = (renta * 12) * (ocupacion / 100)
utilidad = ingreso_anual - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Ingreso Anual Est.", f"${ingreso_anual:,.0f}")
m2.metric("Utilidad Neta", f"${utilidad:,.0f}")
m3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONSULTORÍA CON GROQ (IA) ---
st.divider()
st.subheader("🤖 Belotti AI Consulting")
pregunta = st.text_input("Pregunta al consultor (Ask in English or Spanish):", placeholder="Ej: What is the ROI outlook for this zone?")

if st.button("Analizar con IA"):
    if pregunta:
        if "GROQ_API_KEY" in st.secrets:
            api_key = st.secrets["GROQ_API_KEY"]
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Estructura verificada sin errores de sintaxis
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a certified Real Estate expert in Cancun. MANDATORY: Respond ONLY in the same language the user uses. If the user asks in English, answer in English. If the user asks in Spanish, answer in Spanish."
                    },
                    {
                        "role": "user", 
                        "content": f"Context: Property ${precio} USD, Cap Rate {cap_rate:.2f}%. Question: {pregunta}"
                    }
                ],
                "temperature": 0.5
            }
            
            with st.spinner("Analizando..."):
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=20)
                    if response.status_code == 200:
                        respuesta = response.json()['choices'][0]['message']['content']
                        st.info(respuesta)
                    else:
                        error_msg = response.json().get('error', {}).get('message', 'Error desconocido')
                        st.error(f"Error técnico: {error_msg}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
        else:
            st.error("⚠️ Configura 'GROQ_API_KEY' en los Secrets de Streamlit.")
    else:
        st.warning("Escribe una pregunta para el consultor.")
        st.divider()
st.header("🤖 Asistente IA Belotti Inversiones")
st.info("Pregúntame sobre los resultados de tu cálculo o sobre oportunidades de inversión en la Riviera Maya.")

# Inicializar el historial de mensajes en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes anteriores del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar la pregunta del usuario
if prompt := st.chat_input("¿Qué duda tienes sobre esta inversión?"):
    # Añadir mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar respuesta con Gemini
    with st.chat_message("assistant"):
        with st.spinner("Analizando datos..."):
            # Aquí la IA usa tu perfil trilingüe y certificado
            response = model.generate_content(prompt)
            st.markdown(response.text)
            
    # Añadir respuesta de la IA al historial
    st.session_state.messages.append({"role": "assistant", "content": response.text})
