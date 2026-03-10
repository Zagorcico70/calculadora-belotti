import streamlit as st

def check_password():
    if "password_correct" not in st.session_state:
        st.sidebar.title("🔐 Acceso Privado")
        # Aquí puedes cambiar el texto a español si quieres
        password = st.sidebar.text_input("Introduce el código para acceder:", type="password")
        if st.sidebar.button("Entrar"):
            if password == "Belotti2026": # <--- Esta es tu contraseña
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.sidebar.error("⚠️ Código incorrecto")
        return False
    return True

# ESTA LÍNEA ES CLAVE:
if check_password():

    st.set_page_config(page_title="Belotti Inversiones", layout="centered")

locaciones = {
"Villas Marlin": [21.102437786454768, -86.76195352773082],
"Amara": [21.1685, -86.8010],
"Puerto Cancun": [21.16205146928014, -86.80774264339938],
"La Amada": [21.2585, -86.8115],
}


with st.sidebar:
    
    st.title("Configuración")
    prop = st.text_input("Propiedad / Cliente", value="Villas Marlin")
    pct_cierre = st.slider("Gastos de Cierre e Impuestos %", 5, 6, 7)


st.title(f"Análisis: {prop}")
col1, col2 = st.columns(2)
with col1:
    precio = st.number_input("Precio de Venta (USD)", value=250000, step=10000)
with col2:
    renta = st.number_input("Renta Mensual (USD)", value=2500, step=100)

inversion_total = precio * (1 + (pct_cierre / 100))
utilidad_neta_anual = (renta * 12) * 0.75  # Menos 20% de mantenimiento/administración
roi_final = (utilidad_neta_anual / inversion_total) * 100

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Inversión Total", f"${inversion_total:,.0f}")
m2.metric("Utilidad Anual", f"${utilidad_neta_anual:,.0f}")
m3.metric("ROI REAL NETO", f"{roi_final:.2f}%")

st.subheader("Ubicación Estratégica")
if prop in locaciones:
    punto = locaciones[prop]
    zoom_n = 16
else:
  
    st.divider() 
    st.subheader("📍 Ubicación Estratégica en Cancún")

    # Coordenadas exactas para Puerto Cancún 
    # Lat: 21.1438, Lon: -86.8035
    punto_lat = 21.1438
    punto_lon = -86.8035


    df_mapa = pd.DataFrame({'lat': [punto_lat], 'lon': [punto_lon]})


st.map(df_mapa, zoom=15)


st.link_button("🗺️ Abrir en Google Maps", f"https://www.google.com/maps?q={punto_lat},{punto_lon}")


st.divider()
c1, c2 = st.columns(2)

wa_link = f"https://wa.me/529847454906?text=Info%20sobre%20{prop}"

c_btn1, c_btn2 = st.columns(2)
with c_btn1:
    
    st.link_button("📲 WhatsApp", wa_link, use_container_width=True)
with c_btn2:
    st.link_button("💼 Mi Perfil", "https://www.linkedin.com/in/antonio-belotti-93521a8b/?locale=es")
    st.caption("Antonio Belotti - Real Estate Advisor")
