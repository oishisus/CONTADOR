import streamlit as st
from datetime import datetime
import json
import random
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Reencuentro 💕", page_icon="💖", layout="centered", initial_sidebar_state="collapsed")

# Auto refresco cada 1 segundo
st_autorefresh(interval=1000, key="contador")

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
    .mensaje-especial {
        color: #FF69B4;
        font-size: 1.1em;
        text-align: center;
        font-weight: bold;
        margin: 15px 0;
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
MENSAJE_FILE = DATOS_DIR / "mensaje_principal.json"
NOTAS_FILE = DATOS_DIR / "notas.json"

# Funciones
def cargar_mensaje():
    if MENSAJE_FILE.exists():
        with open(MENSAJE_FILE, 'r', encoding='utf-8') as f:
            datos = json.load(f)
            return datos.get("texto", "")
    return ""

def guardar_mensaje(texto):
    with open(MENSAJE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"texto": texto}, f, ensure_ascii=False, indent=2)

def cargar_notas():
    if NOTAS_FILE.exists():
        with open(NOTAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_notas(notas):
    with open(NOTAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)

# ===== HEADER =====
st.markdown("""
    <div class='header-container'>
        <div class='header-title'>💖 Reencuentro Contador</div>
    </div>
""", unsafe_allow_html=True)

# Foto en header
foto_path = Path("assets/pareja.jpg")
if foto_path.exists():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(str(foto_path), use_container_width=True)

# ===== CONTADOR =====
ahora = datetime.now()
diferencia = fecha_final - ahora

if diferencia.total_seconds() <= 0:
    st.markdown("<div class='contador-small'>💖 ¡Hoy es el día! 💖</div>", unsafe_allow_html=True)
else:
    dias = diferencia.days
    horas, resto = divmod(diferencia.seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    st.markdown(f"<div class='contador-small'>⏳ {dias}d : {horas}h : {minutos}m : {segundos}s</div>", unsafe_allow_html=True)

st.divider()

# ===== NOTAS ALEATORIAS =====
st.subheader("💭 NOTAS ALEATORIAS")
notas = cargar_notas()

if notas:
    lista_notas = list(notas.items())
    random.shuffle(lista_notas)
    
    for clave, nota in lista_notas[:3]:
        st.markdown(f"""
        <div class='nota-random'>
            <div class='nota-header'>📅 {nota.get('fecha', 'N/A')} • {nota.get('usuario', 'N/A')} • {nota.get('hora', 'N/A')}</div>
            <div class='nota-texto'>{nota['texto']}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("📭 Aún no hay notas")

st.divider()

# ===== AGREGAR NOTA =====
st.subheader("✍️ AGREGAR NOTA")

col_user, col_space = st.columns([1, 2])
with col_user:
    usuario = st.selectbox("¿Quién?", ["Belandria", "Segovia"], label_visibility="collapsed")

nota_texto = st.text_area("Tu nota:", height=100, label_visibility="collapsed", placeholder="Escribe tu nota aquí...")

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

# ===== HISTORIAL =====
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
