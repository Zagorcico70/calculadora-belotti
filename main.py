import streamlit as st
import google.generativeai as genai

# Configuración de la página
st.set_page_config(page_title="Belotti AI Consulting", page_icon="🤖")

# --- GESTIÓN SEGURA DE API KEY ---
try:
    # Busca la clave en los Secrets de la plataforma Streamlit
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # Configuración del modelo con un "System Instruction" para que sea experto
    model = genai.GenerativeModel(
        model_name='gemini-pro',
        generation_config={"temperature": 0.7},
    )
except Exception as e:
    st.error("⚠️ Configuración incompleta: No se detectó la clave GEMINI_API_KEY.")
    st.info("Configura la clave en el panel de Streamlit Cloud (Settings > Secrets).")
    st.stop()

# --- INTERFAZ ---
st.title("🤖 Belotti AI Consulting")
st.markdown("---")

# Instrucción del sistema (Invisible para el usuario, pero guía a la IA)
SYSTEM_PROMPT = """
Eres un experto consultor de inversiones inmobiliarias y analista de datos en Cancún. 
Tu objetivo es ayudar a Antonio Belotti a analizar propiedades, calcular ROI, 
Cap Rates y dar certidumbre a inversionistas internacionales. 
Usa un tono profesional, directo y basado en datos reales de Quintana Roo.
"""

# Entrada del usuario
user_query = st.text_area("Describa el escenario de inversión o la duda técnica:", 
                          placeholder="Ej: Calcula el ROI neto para un edificio de $1.15M USD con ingresos de $19k USD mensuales...")

if st.button("Iniciar Consultoría"):
    if user_query:
        with st.spinner("Analizando con Belotti AI..."):
            try:
                # Combinamos el contexto de experto con la duda del usuario
                full_prompt = f"{SYSTEM_PROMPT}\n\nUsuario pregunta: {user_query}"
                response = model.generate_content(full_prompt)
                
                st.subheader("📊 Análisis de Consultoría:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error en la generación: {e}")
    else:
        st.warning("Por favor, ingresa una consulta.")
