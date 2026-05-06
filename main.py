import streamlit as st
import google.generativeai as genai

# 1. Configuración de Seguridad (Usando Gemini)
# Este código busca exclusivamente la etiqueta GEMINI_API_KEY
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Error: Configura 'GEMINI_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 2. Interfaz Profesional de Belotti Analytics
st.set_page_config(page_title="Belotti Analytics", page_icon="📊")
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment Audit - Cancún")

# 3. Calculadora de Inversión (Tus métricas actuales)
col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio Venta (USD)", value=1150000)
    renta = st.number_input("Renta Mensual Bruta (USD)", value=16192)
with col2:
    gastos = st.number_input("Gastos/Mantenimiento (USD)", value=1000)
    ocupacion = st.slider("Ocupación Anual %", 0, 100, 100)

# Cálculos de negocio para Riviera Maya
ingreso_anual = (renta * 12) * (ocupacion / 100)
utilidad_neta = ingreso_anual - (gastos * 12)
cap_rate = (utilidad_neta / precio) * 100

# Resultados Visuales de Belotti Inversiones
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Ingreso Anual Est.", f"${ingreso_anual:,.0f}")
c2.metric("Utilidad Neta", f"${utilidad_neta:,.0f}")
c3.metric("CAP RATE", f"{cap_rate:.2f}%")

# 4. Consultor IA con Identidad de Antonio Belotti
st.divider()
st.subheader("🤖 Belotti AI Consulting")

# Perfil del Asesor (Contexto para la IA)
contexto_antonio = f"""
Eres Antonio Belotti, Real Estate Advisor trilingüe (Italiano, Español, Inglés).
Credenciales:
- Asesor Inmobiliario Certificado por CONOCER (Folio de certificación oficial).
- Experto en Data Analytics e IA (Certificado por Google e IBM).
- Especialista en Cancún y Riviera Maya con más de 5 años de trayectoria.
- Fundador de Belotti Inversiones.

Instrucciones: 
Responde de forma ejecutiva. Si preguntan por los números de arriba, 
menciona el CAP RATE de {cap_rate:.2f}% y la Utilidad de ${utilidad_neta:,.0f}.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Pregunta al consultor (Ask in English or Spanish):"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Usamos el modelo gratuito y potente de Google
        model = genai.GenerativeModel('gemini-1.5-flash')
        full_prompt = f"{contexto_antonio}\n\nPregunta del cliente: {prompt}"
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
