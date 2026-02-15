import streamlit as st
from datetime import datetime
import json
import random
from pathlib import Path
import time

st.set_page_config(page_title="Reencuentro 💕", page_icon="💖", layout="centered", initial_sidebar_state="collapsed")

# CSS personalizado
st.markdown("""
    <style>
    body { background-color: #0a0e27; }
    .header-container {
        text-align: center;
        padding: 20px 0;
    }
    .header-title {
        color: #FF1493;
        font-size: 2.8em;
        font-weight: bold;
        margin: 0;
    }
    .contador-small {
        font-size: 1.5em;
        color: #FF1493;
        text-align: center;
        font-weight: bold;
        margin: 10px 0;
    }
    .nota-random {
        background-color: #1a2647;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 4px solid #FF1493;
    }
    .nota-header {
        color: #FF1493;
        font-weight: bold;
        font-size: 0.9em;
        margin-bottom: 8px;
    }
    .nota-texto {
        color: #e0e0e0;
        font-size: 0.95em;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración
fecha_final = datetime(2026, 6, 14, 0, 0, 0)
DATOS_DIR = Path("datos_reencuentro")
DATOS_DIR.mkdir(exist_ok=True)
NOTAS_FILE = DATOS_DIR / "notas.json"

# ===== HEADER =====
st.markdown("""
    <div class='header-container'>
        <div class='header-title'>💖 Reencuentro Contador</div>
    </div>
""", unsafe_allow_html=True)

# ===== CONTADOR EN TIEMPO REAL =====
placeholder = st.empty()

while True:
    ahora = datetime.now()
    diferencia = fecha_final - ahora

    if diferencia.total_seconds() <= 0:
        placeholder.markdown(
            "<div class='contador-small'>💖 ¡Hoy es el día! 💖</div>",
            unsafe_allow_html=True
        )
        break
    else:
        dias = diferencia.days
        horas, resto = divmod(diferencia.seconds, 3600)
        minutos, segundos = divmod(resto, 60)

        placeholder.markdown(
            f"<div class='contador-small'>⏳ {dias}d : {horas}h : {minutos}m : {segundos}s</div>",
            unsafe_allow_html=True
        )

    time.sleep(1)
