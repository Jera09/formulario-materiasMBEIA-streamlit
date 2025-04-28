import streamlit as st
#from tables import tables as t
#import dataframes
#from charts import charts
from Inicio import inicio 
from MBDEIA import BD_IA as BD
from MEDE import MEDE

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
    st.session_state.menu = st.selectbox("Menu", ["Inicio","Big Data e Inteligencia Artificial", "Estratégia y Dirección de Empresas"])


if st.session_state.menu == "Inicio":
    inicio()
elif st.session_state.menu == "Big Data e Inteligencia Artificial":
    BD()
elif st.session_state.menu == "Estratégia y Dirección de Empresas":
    MEDE()