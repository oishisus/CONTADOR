import streamlit as st
from datetime import datetime
import json
import time
import random
from pathlib import Path

st.set_page_config(page_title="Reencuentro 💕", page_icon="💖", layout="centered", initial_sidebar_state="collapsed")

# CSS personalizado para mejor aspecto
st.markdown("""
    <style>
    .title-container {
        text-align: center;
        margin: 20px 0;
    }
    .title-container h1 {
        color: #FF1493;
        font-size: 2.5em;
        margin: 0;
    }
    .subtitle-text {
        color: #FF69B4;
        font-size: 1.2em;
        font-weight: bold;
        text-align: center;
        margin: 10px 0 20px 0;
    }
    .contador-box {
        background: linear-gradient(135deg, #FF1493 0%, #FF69B4 100%);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin: 20px 0;
    }
    .contador-text {
        font-size: 2em;
        font-weight: bold;
        margin: 10px 0;
    }
    .foto-container {
        margin: 20px 0;
        text-align: center;
    }
    .notes-section {
        margin: 30px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración
fecha_final = datetime(2026, 6, 14, 0, 0, 0)
DATOS_DIR = Path("datos_reencuentro")
DATOS_DIR.mkdir(exist_ok=True)
MENSAJE_FILE = DATOS_DIR / "mensaje_principal.json"
NOTAS_FILE = DATOS_DIR / "notas.json"

# Funciones para manejar mensajes
def cargar_mensaje():
    if MENSAJE_FILE.exists():
        with open(MENSAJE_FILE, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return datos.get("texto", "")
    return ""

def guardar_mensaje(texto):
    with open(MENSAJE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"texto": texto}, f, ensure_ascii=False, indent=2)

# Funciones para manejar notas
def cargar_notas():
    if NOTAS_FILE.exists():
        with open(NOTAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_notas(notas):
    with open(NOTAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)

# TÍTULO
st.markdown("""
    <div class='title-container'>
        <h1>💖 Reencuentro Contador</h1>
    </div>
""", unsafe_allow_html=True)

# MENSAJE ESPECIAL
st.write("✨ Mensaje especial:")
col_msg1, col_msg2 = st.columns([3, 1])
with col_msg1:
    mensaje_actual = cargar_mensaje()
    nuevo_mensaje = st.text_input("", value=mensaje_actual, label_visibility="collapsed", placeholder="Escribe algo especial...")
with col_msg2:
    if st.button("💾 Actualizar", use_container_width=True):
        guardar_mensaje(nuevo_mensaje)
        st.success("✅ Actualizado")
        st.rerun()

st.markdown(f"<p class='subtitle-text'>{cargar_mensaje()}</p>", unsafe_allow_html=True)

st.divider()

# CONTADOR EN TIEMPO REAL
st.subheader("⏳ Tiempo restante")
placeholder_contador = st.empty()

ahora = datetime.now()
diferencia = fecha_final - ahora

if diferencia.total_seconds() <= 0:
    st.success("💖 ¡Hoy es el día! 💖", icon="✅")
else:
    while True:
        ahora = datetime.now()
        diferencia = fecha_final - ahora
        
        if diferencia.total_seconds() <= 0:
            placeholder_contador.success("💖 ¡Hoy es el día! 💖", icon="✅")
            break
        
        dias = diferencia.days
        horas, resto = divmod(diferencia.seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        
        placeholder_contador.markdown(f"""
            <div class='contador-box'>
                <div class='contador-text'>⏳ {dias}d : {horas}h : {minutos}m : {segundos}s</div>
                <p>Cada segundo nos acerca más 💕</p>
            </div>
        """, unsafe_allow_html=True)
        
        time.sleep(1)
        st.rerun()

st.divider()

# NOTAS ALEATORIAS
st.subheader("💭 NOTAS ALEATORIAS")
notas = cargar_notas()

if notas:
    lista_notas = list(notas.items())
    random.shuffle(lista_notas)
    
    for clave, nota in lista_notas[:3]:  # Mostrar solo 3 notas aleatorias
        st.markdown(f"""
        <div style='background-color: #f0f2f6; padding: 15px; border-radius: 8px; margin: 10px 0;'>
            <p style='margin: 0; color: #FF1493; font-weight: bold;'>
                📅 {nota.get('fecha', 'N/A')} • {nota.get('usuario', 'N/A')} • {nota.get('hora', 'N/A')}
            </p>
            <p style='margin: 10px 0 0 0; color: #333;'>{nota['texto']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("📭 Aún no hay notas")

st.divider()

# FOTO
st.subheader("📸 Nosotros")
foto_path = Path("assets/pareja.jpg")
if foto_path.exists():
    st.image(str(foto_path), use_container_width=True)
else:
    st.info("📸 Sube pareja.jpg a assets/")

st.divider()

# NOTAS DIARIAS
st.subheader("✍️ NOTAS DIARIAS")

col_user, col_empty = st.columns([1, 2])
with col_user:
    usuario = st.selectbox("¿Quién escribe?", ["Belandria", "Segovia"], label_visibility="collapsed")

nota_texto = st.text_area("Escribe tu nota:", height=100, label_visibility="collapsed", placeholder="Escribe tu nota aquí...")

if st.button("💾 Guardar nota", use_container_width=True):
    if nota_texto.strip():
        hoy = datetime.now().strftime("%Y-%m-%d")
        notas = cargar_notas()
        clave = f"{hoy}_{usuario}_{datetime.now().strftime('%H%M%S')}"
        
        notas[clave] = {
            "texto": nota_texto,
            "hora": datetime.now().strftime("%H:%M:%S"),
            "fecha": hoy,
            "usuario": usuario
        }
        
        guardar_notas(notas)
        st.success(f"✅ Nota guardada por {usuario}")
        st.balloons()
        st.rerun()
    else:
        st.warning("⚠️ Escribe una nota antes de guardar")

st.divider()

# TODAS LAS NOTAS
st.subheader("📚 TODOS LOS REENCUENTROS")
notas = cargar_notas()

if notas:
    lista_notas = list(notas.items())
    lista_notas.sort(key=lambda x: x[1].get('fecha', ''), reverse=True)
    
    for clave, nota in lista_notas:
        with st.expander(f"📅 {nota.get('fecha', 'N/A')} • {nota.get('usuario', 'N/A')} • {nota.get('hora', 'N/A')}"):
            st.write(nota['texto'])
else:
    st.info("📭 Sin reencuentros aún")