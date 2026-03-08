import streamlit as st

st.set_page_config(page_title="Belotti Inversiones", page_icon="🏝️")

st.title("🏝️ Belotti Real Estate - Cancún")
st.subheader("Calculadora de ROI Inteligente")

# --- ENTRADAS ---
precio = st.number_input("Precio de Venta (USD)", value=250000)
renta_mensual = st.slider("Renta Mensual Estimada (USD)", 500, 15000, 2500)
gastos_pct = st.slider("% Gastos (Mantenimiento, Admin)", 10, 40, 25)

# --- CÁLCULOS ---
utilidad_anual = (renta_mensual * 12) * (1 - (gastos_pct / 100))
roi = (utilidad_anual / precio) * 100

# --- RESULTADOS ---
col1, col2 = st.columns(2)
col1.metric("Utilidad Neta/Año", f"${utilidad_neta:,.0f} USD")
col2.metric("ROI Anual", f"{roi:.2f}%")

st.info(f"Tiempo de recuperación: {precio/utilidad_anual:.1f} años.")
