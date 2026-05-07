import streamlit as st
import requests
import time

st.set_page_config(page_title="Belotti Analytics", page_icon="📊", layout="wide")

# --- ESTILO BELOTTI ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; background-color: #007BFF; color: white; border-radius: 5px; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Belotti Analytics")
st.subheader("Real Estate Investment Audit - Riviera Maya")

# --- CALCULADORA ---
with st.container():
    c1, c2 = st.columns(2)
    with c1:
        precio = st.number_input("Precio de Venta (USD)", value=1150000.0)
        renta = st.number_input("Renta Mensual (USD)", value=19050.0)
    with c2:
        gastos = st.number_input("Gastos Fijos Mensuales (USD)", value=1000.0)
        ocupacion = st.slider("Ocupación Proyectada %", 0, 100, 85)

# Cálculos Financieros
ingreso_anual = (renta * 12) * (ocupacion / 100)
utilidad_neta = ingreso_anual - (gastos * 12)
cap_rate = (utilidad_neta / precio) * 100 if precio > 0 else 0

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Ingreso Anual Bruto", f"${ingreso_anual:,.0f}")
m2.metric("Utilidad Neta (EBITDA)", f"${utilidad_neta:,.0f}")
m3.metric("CAP RATE / ROI", f"{cap_rate:.2f}%")

# --- INTELIGENCIA ARTIFICIAL PROFESIONAL ---
st.divider()
st.subheader("🤖 Consultoría Belotti AI")
pregunta = st.text_input("Haz una pregunta estratégica al asistente:", placeholder="Ej: ¿Por qué este ROI es superior al promedio en la Zona Hotelera?")

if st.button("GENERAR ANÁLISIS ESTRATÉGICO"):
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        st.error("Error: Configura la API Key en Streamlit Secrets.")
    else:
        # Usamos el modelo 1.5 Flash (el mejor balance costo/velocidad)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        contexto = (
            f"Eres Antonio Belotti, un Asesor Inmobiliario Certificado y Data Analyst en Cancún. "
            f"Tu misión es proteger el patrimonio del cliente. Datos actuales: "
            f"Propiedad de ${precio:,.0f} USD, ROI del {cap_rate:.2f}%. "
            f"Contexto local: El Puente Nichupté ya está operando (mayo 2026), facilitando el acceso a la Zona Hotelera. "
            f"Responde de forma profesional, técnica y persuasiva a: {pregunta}"
        )
        
        payload = {"contents": [{"parts": [{"text": contexto}]}]}
        
        with st.spinner("Belotti AI está procesando los datos de mercado..."):
            intentos = 0
            while intentos < 3:
                try:
                    res = requests.post(url, json=payload, timeout=20)
                    if res.status_code == 200:
                        st.success("**Análisis Profesional:**")
                        st.write(res.json()['candidates'][0]['content']['parts'][0]['text'])
                        break
                    elif res.status_code == 503:
                        intentos += 1
                        time.sleep(2)
                        if intentos == 3:
                            st.warning("Google tiene alta demanda. Si habilitaste el pago, esto no debería ocurrir. Reintenta en un momento.")
                    else:
                        st.error(f"Error {res.status_code}: Revisa si la facturación está activa en Google Cloud.")
                        break
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
                    break
