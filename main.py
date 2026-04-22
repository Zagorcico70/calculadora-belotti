import streamlit as st
import pandas as pd
import google.generativeai as genai

# 1. CONFIGURACIÓN DE LA API KEY (Asegúrate de que esté en los Secrets de Streamlit)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Configuración pendiente: Agrega GOOGLE_API_KEY en los Secrets de Streamlit.")

# 2. SISTEMA DE SEGURIDAD (Contraseña)
def check_password():
    def password_entered():
        if st.session_state["password"] == "Cancun2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Introduce la clave de acceso profesional:", type="password", on_change=password_entered, key="password")
        st.info("Esta herramienta es de uso exclusivo para clientes de Antonio Belotti.")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Clave incorrecta. Intenta de nuevo:", type="password", on_change=password_entered, key="password")
        st.error("🔒 Acceso denegado.")
        return False
    else:
        return True

# 3. CUERPO PRINCIPAL DE LA APLICACIÓN
if check_password():
    # Creamos las pestañas principales
    tab1, tab2 = st.tabs(["📊 Calculadora de Inversión", "🛡️ Consultoría IA / Certeza Jurídica"])

    # --- PESTAÑA 1: CALCULADORA ---
    with tab1:
        st.title("📊 Calculadora de Inversión Belotti")
        
        precio = st.number_input("Precio de la Propiedad (USD)", value=1250000)
        renta_mensual = st.number_input("Renta Mensual Estimada (USD)", value=6500)
        zona_mapa = st.selectbox("📍 Ubicación:", ["Puerto Cancún", "Villas Marlin", "Amara", "La Amada"])

        # Lógica de ubicación
        if "Puerto" in zona_mapa:
            lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1606, -86.8074, 15, "Puerto Cancún", 9.5
            perfil_txt = "💎 **Estrategia:** Preservación de Capital."
        elif "Marlin" in zona_mapa:
            lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1033, -86.7619, 15, "Villas Marlin", 6.0
            perfil_txt = "🏖️ **Estrategia:** Cash Flow Turístico."
        else:
            lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1619, -86.8515, 12, "Cancún", 5.0
            perfil_txt = "Análisis general."

        # Cálculos rápidos
        gastos_c = precio * 0.06
        inv_total = precio + gastos_c
        roi_n = (((renta_mensual * 12) - 6000) / inv_total) * 100
        
        st.metric("ROI NETO + PLUSVALÍA", f"{(roi_n + plusvalia_num):.2f}%")
        st.info(perfil_txt)
        
        df_m = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(df_m, zoom=zoom_mapa)

    # --- PESTAÑA 2: CHATBOT DE IA ---
    with tab2:
        st.title("🛡️ Consultoría IA / Certeza Jurídica")
        st.markdown("Consulta datos del **PMDU**, el **Fideicomiso** y nuestra **Base de Conocimientos**.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Mostrar historial
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Entrada de chat
        if prompt := st.chat_input("Ej: ¿Qué es un fideicomiso para extranjeros?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Configuración del modelo
            instruccion_ia = (
                "Eres Belotti Analytics, experto de Antonio Belotti. "
                "Tu misión es dar CERTEZA JURÍDICA. Usa el PMDU 2018-2030 para temas legales de Cancún "
                "y el archivo de fideicomiso para explicar la inversión extranjera. "
                "Si no sabes algo, invita al cliente a contactar a Antonio."
            )

            try:
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash",
                    system_instruction=instruccion_ia
                )
                
                with st.chat_message("assistant"):
                    with st.spinner("Consultando bases de datos..."):
                        response = model.generate_content(prompt)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Hubo un problema con la conexión de IA. Verifica tu API Key.")

    # Pie de página compartido
    st.divider()
    st.caption("🚀 **Antonio Belotti** | Real Estate Data Analyst & Certified Agent")
    st.caption("📜 Certificación CONOCER: **D-0012504124**")
