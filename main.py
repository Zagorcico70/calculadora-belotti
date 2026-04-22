import streamlit as st
import pandas as pd
import google.generativeai as genai

# CONFIGURACIÓN DE GEMINI (Requiere que pongas tu clave en los Secrets de Streamlit Cloud)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Falta la configuración de GOOGLE_API_KEY en los Secrets.")

def check_password():
    """Retorna True si el usuario ingresó la contraseña correcta."""
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

if check_password():
    # CREACIÓN DE PESTAÑAS
    tab1, tab2 = st.tabs(["📊 Calculadora de Inversión", "🛡️ Consultoría IA / Certeza Jurídica"])

    with tab1:
        st.title("📊 Calculadora de Inversión Belotti")
        
        precio = st.number_input("Precio de la Propiedad (USD)", value=1250000)
        renta_mensual = st.number_input("Renta Mensual Estimada (USD)", value=6500)
        zona_mapa = st.selectbox("📍 Ubicación:", ["Puerto Cancún", "Villas Marlin", "Amara", "La Amada"])

        # Lógica de ubicación y cálculos (tu código original)
        if "Puerto" in zona_mapa:
            lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1606, -86.8074, 15, "Puerto Cancún", 9.5
            perfil_txt = "💎 **Estrategia:** Preservación de Capital."
        elif "Marlin" in zona_mapa:
            lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1033, -86.7619, 15, "Villas Marlin", 6.0
            perfil_txt = "🏖️ **Estrategia:** Cash Flow Turístico."
        else:
            lat, lon, zoom_mapa, lugar, plusvalia_num = 21.1619, -86.8515, 12, "Cancún", 5.0
            perfil_txt = "Análisis general."

        # Cálculos de ROI
        gastos_escrituracion = precio * 0.06
        inversion_total = precio + gastos_escrituracion
        renta_neta_anual = (renta_mensual * 12) - 6000 # Simplificado para el ejemplo
        roi_porcentaje = (renta_neta_anual / inversion_total) * 100
        retorno_total = roi_porcentaje + plusvalia_num

        st.metric(label="RETORNO TOTAL (ROI + Plusvalía)", value=f"{retorno_total:.2f}%")
        st.info(perfil_txt)
        
        # Mapa
        df_mapa = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(df_mapa, zoom=zoom_mapa)

    with tab2:
        st.title("🛡️ Consultoría IA / Certeza Jurídica")
        st.write("Consulta datos del PMDU 2018-2030 y proyecciones de inversión.")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ej: ¿Qué densidad permite el PMDU en la SM 15?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Instrucciones del Sistema para que use tus archivos
            system_instruction = (
                
                "Eres Belotti Analytics, experto de Antonio Belotti. "
                "Usa el PMDU para temas legales de Cancún y 'TRUST INFO' para explicar el fideicomiso. "
                "Responde con precisión técnica y profesionalismo."
            )

            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash", 
                system_instruction=system_instr
            )
            
            with st.chat_message("assistant"):
                with st.spinner("Analizando bases de datos..."):
                    response = model.generate_content(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})

    # Pie de página (Compartido)
    st.write("---")
    st.caption("🚀 **Antonio Belotti** | Real Estate Data Analyst & Certified Agent")
