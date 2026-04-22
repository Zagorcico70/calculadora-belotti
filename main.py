import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. Configuración de la API (Forzamos la versión estable)
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

# 3. Interfaz
tab1, tab2 = st.tabs(["📊 Calculadora", "🛡️ Consultoría IA"])

with tab1:
    st.title("📊 Calculadora de Inversión")
    precio = st.number_input("Precio Propiedad (USD)", value=1250000)
    renta = st.number_input("Renta Mensual (USD)", value=6500)
    inv_total = precio * 1.06
    roi = (((renta * 12) - 6000) / inv_total) * 100
    st.metric("ROI Estimado", f"{roi:.2f}%")

with tab2:
    st.title("🛡️ Consultoría IA")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for m in st.session_state.messages:
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

    if prompt := st.chat_input("Escribe tu duda..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        try:
            # EL AJUSTE MAESTRO: Usamos 'gemini-pro' que es el nombre universal
            # Este modelo no falla con el error 404 de versiones
            model = genai.GenerativeModel(model_name="gemini-pro")
            
            response = model.generate_content(prompt)
            
            with st.chat_message("assistant"):
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Ajustando conexión... Intenta de nuevo. (Detalle: {str(e)})")
