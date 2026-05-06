import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de Identidad y Seguridad (Secrets)
# Asegúrate de tener GEMINI_API_KEY en los Secrets de Streamlit
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. Configuración de la Interfaz Profesional
st.set_page_config(page_title="Belotti Analytics", page_icon="📊")
st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment Audit - Cancún")

# 3. Calculadora de Inversión (Tus datos actuales)
col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio Venta (USD)", value=1150000)
    renta = st.number_input("Renta Mensual Bruta (USD)", value=16192)
with col2:
    gastos = st.number_input("Gastos/Mantenimiento (USD)", value=1000)
    ocupacion = st.slider("Ocupación Anual %", 0, 100, 100)

# Cálculos de Belotti Inversiones
ingreso_anual = (renta * 12) * (ocupacion / 100)
utilidad_neta = ingreso_anual - (gastos * 12)
cap_rate = (utilidad_neta / precio) * 100

# Resultados Visuales
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("Ingreso Anual Est.", f"${ingreso_anual:,.0f}")
c2.metric("Utilidad Neta", f"${utilidad_neta:,.0f}")
c3.metric("CAP RATE", f"{cap_rate:.2f}%")

# 4. Asistente IA con Identidad de Antonio Belotti
st.divider()
st.subheader("🤖 Belotti AI Consulting")

# Contexto de Identidad (Tu Perfil Profesional)
contexto_antonio = f"""
Eres Antonio Belotti, un reconocido Real Estate Advisor trilingüe (Italiano, Español, Inglés).
Tus credenciales son:
- Asesor Inmobiliario Certificado por CONOCER (no AMPI).
- Certificado en Data Analytics e IA por Google e IBM.
- Más de 5 años de experiencia en el mercado de Cancún y Riviera Maya.
- Fundador de Belotti Inversiones.

Instrucciones:
Responde siempre con profesionalismo. Si te preguntan por el negocio actual, 
usa estos datos: CAP RATE de {cap_rate:.2f}%, Utilidad Neta de ${utilidad_neta:,.0f}.
Explica por qué un CAP RATE arriba del 15% es excepcional en Cancún.
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
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Combinamos el contexto con la pregunta
        response = model.generate_content(f"{contexto_antonio}\n\nUsuario dice: {prompt}")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
