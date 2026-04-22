import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. Configuración de la API
api_key = st.secrets.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("🚨 Falta la clave en Secrets.")

# 2. Seguridad
if "auth" not in st.session_state:
    st.title("🔐 Belotti Inversiones")
    pwd = st.text_input("Contraseña:", type="password")
    if st.button("Entrar"):
        if pwd == "Cancun2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Clave incorrecta")
    st.stop()

# 3. Aplicación Principal
tab1, tab2 = st.tabs(["📊 Calculadora", "🛡️ Consultoría IA"])

with tab1:
    st.title("📊 Calculadora de Inversión")
    precio = st.number_input("Precio Propiedad (USD)", value=1250000)
    renta = st.number_input("Renta Mensual (USD)", value=6500)
    
    # Cálculos básicos
    inv_total = precio * 1.06 # Precio + 6% gastos
    roi = (((renta * 12) - 6000) / inv_total) * 100
    st.metric("ROI Estimado", f"{roi:.2f}%")
    st.write("Ubicación: Cancún, MX")

with tab2:
    st.title("🛡️ Consultoría IA")
    st.info("Asistente legal y técnico de Belotti Inversiones.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Pregunta sobre el PMDU o Fideicomiso..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            # EL CAMBIO CLAVE: Usamos el modelo 'flash' que es el compatible
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error técnico: {str(e)}")
