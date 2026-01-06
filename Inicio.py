import streamlit as st
import pandas as pd

def inicio():

    st.header("Lista de formularios para selección de materias")
    st.subheader("Instrucciones: ")
    st.write("")
    st.write("#### Del menu selecciona el programa de maestría al que perteneces. Dentro encontraras una serie de instrucciones, las cuales dependerán del programa al que perteneces. ####")
    st.write("#### Por favor tomate tu tiempo para realizar la selección, en caso de tener alguna duda contacta a tu coordinador. ####")
    datos = [
        ["Finanzas Estratégicas y Análisis de Negocios", "Juan Manuel Pérez Cruz", "manuel.perezcr@anahuac.mx"],
        ["Mercadotecnia y Comunicación Estratégica", "Juan Manuel Pérez Cruz", "manuel.perezcr@anahuac.mx"],
        ["Dirección Estratégica del Talento Humano", "Juan Manuel Pérez Cruz", "manuel.perezcr@anahuac.mx"],
        ["Administración y Gestión Publica", "Karenm Ramírez Barbosa", "karenm.ramirezba@anahuac.mx"],
        ["Estratégia y  Dirección de Empresas", "Armando Uriel García Santana", "armandou.garciasa@anahuac.mx"],
        ["Innovación, Emprendimiento y Dirección de Tecnología", "Armando Uriel García Santana", "armandou.garciasa@anahuac.mx"],
        ["Derecho Empresarial y Gobierno Corporativo", "Karenm Ramírez Barbosa", "karenm.ramirezba@anahuac.mx"],
        ["Dirección Estratégica de Instituciones de Salud", "Armando Uriel García Santana", "armandou.garciasa@anahuac.mx"],
        ["Big Data e Inteligencia Artificial", "José de Jesús Ramos Beltrán", "jesus.ramosb@anahuac.mx"],
        ["Ingeniería para la Dirección de Operaciones", "José de Jesús Ramos Beltrán", "jesus.ramosb@anahuac.mx"]
    ]

    df = pd.DataFrame(datos, columns=['PROGRAMA', 'COORDINADOR', 'CORREO'])

    st.table(df)

