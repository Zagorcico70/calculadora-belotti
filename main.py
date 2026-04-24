import streamlit as st
import requests

st.title("🛠️ Diagnóstico Belotti Analytics")

if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    # Esta URL le pide a Google la lista de modelos que TU llave puede usar
    url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
    
    if st.button("Verificar mi Llave"):
        response = requests.get(url)
        data = response.json()
        
        if "models" in data:
            st.success("✅ Tu llave funciona. Estos son tus modelos disponibles:")
            for m in data["models"]:
                st.write(f"- {m['name']}")
        else:
            st.error("❌ Tu llave NO tiene acceso a ningún modelo.")
            st.json(data)
else:
    st.error("No hay API Key en Secrets.")
