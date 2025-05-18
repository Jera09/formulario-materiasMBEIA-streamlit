import streamlit as st
from Inicio import inicio 
from MBDEIA import BD_IA
from MEDE import MEDE
from MMyCE import mmyce
from MFEAN import MFEAN
from MDTH import MDTH
from MIDO import MIDO

# Configuración inicial
st.set_page_config(
    page_title="Formulario de Registro de Materias",
    layout="wide",
    page_icon="A.png"
)

#Logo (Agregar imagen de fondo)
st.image("A.png", width=200)

if "menu" not in st.session_state:
    st.session_state.menu = "Inicio"

with st.sidebar:
    st.session_state.menu = st.selectbox("Menu", ["Inicio","Big Data e Inteligencia Artificial", "Estratégia y Dirección de Empresas", "Mercadotecnia y Comunicación Estratégica", "Finanzas Estratégicas y Análisis de Negocios", "Dirección Estratégica del Talento Humano", "Ingeniería para la Dirección de Operaciones"])


if st.session_state.menu == "Inicio":
    inicio()
elif st.session_state.menu == "Big Data e Inteligencia Artificial":
    BD_IA()
elif st.session_state.menu == "Estratégia y Dirección de Empresas":
    MEDE()
elif st.session_state.menu == "Mercadotecnia y Comunicación Estratégica":
    mmyce()
elif st.session_state.menu == "Finanzas Estratégicas y Análisis de Negocios":
    MFEAN()
elif st.session_state.menu == "Dirección Estratégica del Talento Humano":
    MDTH()
elif st.session_state.menu == "Ingeniería para la Dirección de Operaciones":
    MIDO()
