import streamlit as st
import google.generativeai as genai

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Belotti Analytics", page_icon="📊")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    # Probamos con el modelo más nuevo y estable de 2026
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Falta la API Key en los Secrets.")
    st.stop()

# --- CALCULADORA ---
st.title("📊 Belotti Analytics")
c1, c2 = st.columns(2)
with c1:
    precio = st.number_input("Precio Venta (USD)", value=1150000.0)
    renta = st.number_input("Renta Mensual (USD)", value=19050.0)
with c2:
    gastos = st.number_input("Gastos Mensuales (USD)", value=1000.0)
    ocupacion = st.slider("Ocupación %", 0, 100, 70)

utilidad = (renta * 12 * (ocupacion/100)) - (gastos * 12)
cap_rate = (utilidad / precio) * 100 if precio > 0 else 0

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Ingreso Anual", f"${(renta * 12 * (ocupacion/100)):,.2f}")
m2.metric("Utilidad Neta", f"${utilidad:,.2f}")
m3.metric("CAP RATE", f"{cap_rate:.2f}%")

# --- CONSULTORÍA ---
st.divider()
st.subheader("🤖 Consultoría IA Belotti")
pregunta = st.text_input("¿Qué quieres analizar?", placeholder="Ej: Argumentos de venta para este ROI")

if st.button("Analizar con IA"):
    if pregunta:
        with st.spinner("Analizando..."):
            try:
                # Prompt enriquecido con tu perfil experto
                prompt = f"Como experto inmobiliario en Cancún, analiza: Precio ${precio}, Cap Rate {cap_rate:.2f}%. Pregunta: {pregunta}"
                response = model.generate_content(prompt)
                st.info(response.text)
            except Exception as e:
                # Si falla el 1.5-flash, el código nos dirá por qué
                st.error(f"Nota: Estamos ajustando la conexión. Error: {e}")
    else:
        st.warning("Escribe una pregunta.")
