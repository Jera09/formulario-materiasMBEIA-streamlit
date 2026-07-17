import streamlit as st

# Configuración inicial de la página (DEBE ser el primer comando de Streamlit)
st.set_page_config(
    page_title="Formulario de Registro de Materias",
    layout="wide",
    page_icon="A.png"
)

# -----------------------------------------------------------------------------
# OPTIMIZACIÓN DE MEMORIA Y IMAGEN (Evita choques en el disco de Render)
# -----------------------------------------------------------------------------
@st.cache_resource
def cargar_logo():
    # Cacheamos el recurso de imagen para que no choque en el disco
    # al abrir múltiples navegadores simultáneamente.
    return "A.png"

try:
    st.image(cargar_logo(), width=200)
except Exception:
    pass  # Si falta la imagen en el servidor, no detiene la aplicación

# -----------------------------------------------------------------------------
# BARRA LATERAL Y NAVEGACIÓN (Corregido para multisesión segura)
# -----------------------------------------------------------------------------
with st.sidebar:
    st.selectbox(
        "Menu", 
        [
            "Inicio",
            "Big Data e Inteligencia Artificial", 
            "Estratégia y Dirección de Empresas", 
            "Mercadotecnia y Comunicación Estratégica", 
            "Finanzas Estratégicas y Análisis de Negocios", 
            "Dirección Estratégica del Talento Humano", 
            "Ingeniería para la Dirección de Operaciones", 
            "Innovación, Emprendimiento y Dirección de Tecnología", 
            "Derecho Empresarial y Gobierno Corporativo", 
            "Administración y Gestión Pública", 
            "Dirección Estratégica de Instituciones de Salud"
        ],
        key="menu"  # <-- Esto conecta de forma nativa y segura con st.session_state.menu
    )

# -----------------------------------------------------------------------------
# ENRUTAMIENTO CON LAZY LOADING (Carga solo el módulo que se usa en el momento)
# -----------------------------------------------------------------------------
menu_actual = st.session_state.menu

if menu_actual == "Inicio":
    from Inicio import inicio 
    inicio()

elif menu_actual == "Big Data e Inteligencia Artificial":
    from MBDEIA import BD_IA
    BD_IA()

elif menu_actual == "Estratégia y Dirección de Empresas":
    from MEDE import MEDE
    MEDE()

elif menu_actual == "Mercadotecnia y Comunicación Estratégica":
    from MMyCE import mmyce
    mmyce()

elif menu_actual == "Finanzas Estratégicas y Análisis de Negocios":
    from MFEAN import MFEAN
    MFEAN()

elif menu_actual == "Dirección Estratégica del Talento Humano":
    from MDTH import MDTH
    MDTH()

elif menu_actual == "Ingeniería para la Dirección de Operaciones":
    from MIDO import MIDO
    MIDO()

elif menu_actual == "Innovación, Emprendimiento y Dirección de Tecnología":
    from MIEDT import MIEDT
    MIEDT()

elif menu_actual == "Derecho Empresarial y Gobierno Corporativo":
    from MDEGC import MDEGC
    MDEGC()

elif menu_actual == "Administración y Gestión Pública":
    from MAGP import MAGP
    MAGP()

elif menu_actual == "Dirección Estratégica de Instituciones de Salud":
    from MDEIS import MDEIS
    MDEIS()
