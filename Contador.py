import streamlit as st
from datetime import datetime
import time
import json
import os
from pathlib import Path

st.set_page_config(page_title="Reencuentro 💕", page_icon="💖", layout="wide")

st.title("💖 Cuenta regresiva para nuestro reencuentro")

# Configuración
fecha_final = datetime(2026, 6, 14, 0, 0, 0)
DATOS_DIR = Path("datos_reencuentro")
NOTAS_FILE = DATOS_DIR / "notas.json"
FOTOS_DIR = DATOS_DIR / "fotos"

# Crear directorios si no existen
DATOS_DIR.mkdir(exist_ok=True)
FOTOS_DIR.mkdir(exist_ok=True)

# Funciones para manejar notas
def cargar_notas():
    if NOTAS_FILE.exists():
        with open(NOTAS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_notas(notas):
    with open(NOTAS_FILE, 'w', encoding='utf-8') as f:
        json.dump(notas, f, ensure_ascii=False, indent=2)

def hay_nota_hoy():
    hoy = datetime.now().strftime("%Y-%m-%d")
    notas = cargar_notas()
    return hoy in notas

# Contar regresiva (sin loop infinito para mejor rendimiento)
col1, col2 = st.columns(2)

with col1:
    st.subheader("⏳ Tiempo restante")
    placeholder = st.empty()

ahora = datetime.now()
diferencia = fecha_final - ahora

if diferencia.total_seconds() <= 0:
    st.success("💖 ¡Hoy es el día! 💖", icon="✅")
else:
    dias = diferencia.days
    horas, resto = divmod(diferencia.seconds, 3600)
    minutos, segundos = divmod(resto, 60)
    
    st.markdown(
        f"<h2 style='text-align: center; color: #FF1493;'>"
        f"⏳ {dias}d : {horas}h : {minutos}m : {segundos}s"
        f"</h2><p style='text-align: center; color: #FF69B4;'>Cada segundo nos acerca más 💕</p>",
        unsafe_allow_html=True
    )

st.divider()

# Sección de notas diarias
st.subheader("📝 Notas Diarias")

col1, col2 = st.columns(2)

with col1:
    st.write("✍️ Añade una nota para hoy:")
    nota_texto = st.text_area("Escribe tu nota aquí", height=120, key="nota_input")
    
    uploaded_file = st.file_uploader(
        "📸 Sube una foto para hoy", 
        type=["jpg", "jpeg", "png", "gif"],
        key="foto_upload"
    )
    
    if st.button("💾 Guardar nota de hoy", use_container_width=True):
        if nota_texto.strip():
            hoy = datetime.now().strftime("%Y-%m-%d")
            notas = cargar_notas()
            
            # Guardar la nota
            notas[hoy] = {
                "texto": nota_texto,
                "hora": datetime.now().strftime("%H:%M:%S"),
                "tiene_foto": False
            }
            
            # Guardar la foto si existe
            if uploaded_file is not None:
                ext = uploaded_file.name.split('.')[-1]
                foto_path = FOTOS_DIR / f"{hoy}.{ext}"
                with open(foto_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                notas[hoy]["tiene_foto"] = True
                notas[hoy]["foto_ext"] = ext
            
            guardar_notas(notas)
            st.success(f"✅ Nota guardada para {hoy}")
            st.rerun()
        else:
            st.warning("⚠️ Por favor escribe una nota antes de guardar")

with col2:
    st.write("📚 Todas tus notas:")
    notas = cargar_notas()
    
    if notas:
        # Ordenar por fecha descendente
        fechas_ordenadas = sorted(notas.keys(), reverse=True)
        
        for fecha in fechas_ordenadas:
            nota = notas[fecha]
            with st.expander(f"📅 {fecha} - {nota.get('hora', 'N/A')}", expanded=(fecha == datetime.now().strftime("%Y-%m-%d"))):
                st.write(f"**Nota:** {nota['texto']}")
                
                # Mostrar foto si existe
                if nota.get('tiene_foto', False):
                    ext = nota.get('foto_ext', 'jpg')
                    foto_path = FOTOS_DIR / f"{fecha}.{ext}"
                    if foto_path.exists():
                        st.image(str(foto_path), caption=f"Foto del {fecha}")
    else:
        st.info("📭 Aún no hay notas. ¡Crea la primera hoy!")