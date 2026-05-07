# --- CONSULTORÍA CON GEMINI (PETICIÓN DIRECTA) ---
st.divider()
st.subheader("🤖 Belotti AI Consulting")
pregunta = st.text_input("Pregunta al consultor (Ask in English or Spanish):", placeholder="Ej: What is the ROI outlook for this zone?")

if st.button("Analizar con IA"):
    if pregunta:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
            # Usamos el endpoint directo de la API para evitar errores de librería
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            
            headers = {'Content-Type': 'application/json'}
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": (
                            f"You are a certified Real Estate expert in Cancun. "
                            f"MANDATORY: Respond ONLY in the same language the user uses. "
                            f"Context: Property Price ${precio} USD, Cap Rate {cap_rate:.2f}%. "
                            f"Question: {pregunta}"
                        )
                    }]
                }]
            }
            
            with st.spinner("Analizando..."):
                try:
                    response = requests.post(url, headers=headers, json=payload, timeout=20)
                    if response.status_code == 200:
                        # Extraemos la respuesta del formato JSON de Google
                        respuesta = response.json()['candidates'][0]['content']['parts'][0]['text']
                        st.info(respuesta)
                    else:
                        st.error(f"Error de API: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
        else:
            st.error("⚠️ Configura 'GEMINI_API_KEY' en los Secrets.")
    else:
        st.warning("Escribe una pregunta.")
