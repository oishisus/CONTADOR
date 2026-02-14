import streamlit as st
from datetime import datetime
import time

st.set_page_config(page_title="Reencuentro 💕", page_icon="💖")

st.title("💖 Cuenta regresiva para nuestro reencuentro")

# Fecha fija
fecha_final = datetime(2026, 6, 14, 0, 0, 0)

placeholder = st.empty()

while True:
    ahora = datetime.now()
    diferencia = fecha_final - ahora

    if diferencia.total_seconds() <= 0:
        placeholder.success("💖 ¡Hoy es el día! 💖")
        break

    dias = diferencia.days
    horas, resto = divmod(diferencia.seconds, 3600)
    minutos, segundos = divmod(resto, 60)

    placeholder.markdown(
        f"## ⏳ {dias}d : {horas}h : {minutos}m : {segundos}s\n\nCada segundo nos acerca más 💕"
    )

    time.sleep(1)
    st.rerun()