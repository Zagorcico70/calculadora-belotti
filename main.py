import streamlit as st
import google.generativeai as genai

# 1. Intentar leer la clave
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("🚨 ERROR: No pegaste la clave en los Secrets de Streamlit.")

# 2. Entrada con contraseña
if "auth" not in st.session_state:
    clave = st.text_input("Contraseña de acceso:", type="password")
    if clave == "Cancun2026":
        st.session_state.auth = True
        st.rerun()
    st.stop()

# 3. Interfaz del Chat
st.title("🛡️ Consultoría IA Belotti")
if prompt := st.chat_input("Hazme una pregunta técnica:"):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    try:
        # Intentamos conectar con el modelo PRO que es el más potente
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
    except Exception as e:
        # AQUÍ ESTÁ EL TRUCO: Nos dirá el error exacto de Google
        st.error(f"⚠️ ERROR TÉCNICO REAL: {str(e)}")
        st.info("Copia este error y dímelo para saber qué falta en tu cuenta de Google.")
