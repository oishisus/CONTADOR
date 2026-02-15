import streamlit as st
from datetime import datetime
import json
import time
from pathlib import Path

st.set_page_config(page_title="Reencuentro 💕", page_icon="💖", layout="centered", initial_sidebar_state="collapsed")

# Seleccionar usuario
st.write("👤 ¿Quién eres?")
usuario = st.radio("Selecciona tu nombre:", ["Belandria", "Segovia"], horizontal=True, label_visibility="collapsed")

st.divider()

# Título con foto
col1, col2 = st.columns([1, 1], gap="medium")

with col1:
    st.title("💖 Reencuentro")

with col2:
    # Mostrar foto si existe
    foto_path = Path("assets/pareja.jpg")
    if foto_path.exists():
        st.image(str(foto_path), use_container_width=True)

# Configuración
fecha_final = datetime(2026, 6, 14, 0, 0, 0)
DATOS_DIR = Path("datos_reencuentro")
DATOS_DIR.mkdir(exist_ok=True)
NOTAS_FILE = DATOS_DIR / f"notas_{usuario.lower()}.json"
MENSAJE_FILE = DATOS_DIR / "mensaje_principal.json"

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

# Mostrar y editar mensaje principal
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

st.markdown(f"<p style='text-align: center; color: #FF69B4; font-size: 18px; font-weight: bold;'>{cargar_mensaje()}</p>", unsafe_allow_html=True)

st.divider()

# Contar regresiva en tiempo real
st.subheader("⏳ Tiempo restante")

placeholder_contador = st.empty()

ahora = datetime.now()
diferencia = fecha_final - ahora

if diferencia.total_seconds() <= 0:
    st.success("💖 ¡Hoy es el día! 💖", icon="✅")
else:
    # Mostrar el contador y actualizarlo cada segundo
    while True:
        ahora = datetime.now()
        diferencia = fecha_final - ahora
        
        if diferencia.total_seconds() <= 0:
            placeholder_contador.success("💖 ¡Hoy es el día! 💖", icon="✅")
            break
        
        dias = diferencia.days
        horas, resto = divmod(diferencia.seconds, 3600)
        minutos, segundos = divmod(resto, 60)
        
        placeholder_contador.markdown(
            f"<h2 style='text-align: center; color: #FF1493;'>"
            f"⏳ {dias}d : {horas}h : {minutos}m : {segundos}s"
            f"</h2><p style='text-align: center; color: #FF69B4;'>Cada segundo nos acerca más 💕</p>",
            unsafe_allow_html=True
        )
        
        time.sleep(1)
        st.rerun()

st.divider()

# Sección de notas diarias
st.subheader(f"📝 Mis notas ({usuario})")

st.write("✍️ Añade una nota para hoy:")
nota_texto = st.text_area("Escribe tu nota aquí", height=100, label_visibility="collapsed")

if st.button("💾 Guardar nota de hoy", use_container_width=True):
    if nota_texto.strip():
        hoy = datetime.now().strftime("%Y-%m-%d")
        notas = cargar_notas()
        
        # Guardar la nota
        notas[hoy] = {
            "texto": nota_texto,
            "hora": datetime.now().strftime("%H:%M:%S"),
            "usuario": usuario
        }
        
        guardar_notas(notas)
        st.success(f"✅ Nota guardada para {hoy}")
        st.rerun()
    else:
        st.warning("⚠️ Por favor escribe una nota antes de guardar")

st.divider()

st.write("📚 Todas mis notas:")
notas = cargar_notas()

if notas:
    # Ordenar por fecha descendente
    fechas_ordenadas = sorted(notas.keys(), reverse=True)
    
    for fecha in fechas_ordenadas:
        nota = notas[fecha]
        with st.expander(f"📅 {fecha} - {nota.get('hora', 'N/A')}", expanded=(fecha == datetime.now().strftime("%Y-%m-%d"))):
            st.write(f"**Nota:** {nota['texto']}")
else:
    st.info("📭 Aún no hay notas. ¡Crea la primera hoy!")