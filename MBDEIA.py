import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.platypus import Image

def BD_IA():

    if 'download_data' not in st.session_state:
        st.session_state.download_data = None

    if 'download_data' not in st.session_state:
        st.session_state.download_data = None

    # Configuración inicial
    #st.set_page_config(
    #    page_title="Formulario de Registro de Materias",
    #    layout="wide",
    #    page_icon="A.png"
    #)

    #Logo (Agregar imagen de fondo)
    #st.image("A.png", width=200)

    # Configuración Google Sheets
    def setup_gsheets():
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        try:
            creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
            client = gspread.authorize(creds)
            return client
        except Exception as e:
            st.error(f"Error de conexión: {str(e)}")
            return None

    def save_to_gsheets(data_rows):
        try:
            client = setup_gsheets()
            if not client:
                return False
            
            spreadsheet = client.open("Registro_Materias_Maestria")
            
            try:
                worksheet = spreadsheet.worksheet("Registros")
            except gspread.exceptions.WorksheetNotFound:
                worksheet = spreadsheet.add_worksheet(title="Registros", rows=10000, cols=12)
                # Encabezados actualizados según tu ejemplo de Excel
                worksheet.append_row([
                    "Programa", "ID", "Nombre", "Materia", 
                    "Créditos", "Curso", "Clave", "Nombre de la Materia",
                    "Timestamp", "Teléfono", "Correo", "Género"
                ])
            
            # Insertar todas las filas (una por materia)
            for row in data_rows:
                worksheet.append_row(row)
            
            return True
        except Exception as e:
            st.error(f"Error al guardar: {str(e)}")
            return False

    # Áreas de competencia y materias
    areas_competencias = {
        "Dirección y Liderazgo": [
            {"materia": "Negociación estratégica*", "curso": "LDR", "clave": "55705", "créditos": 6},
            {"materia": "Competencias de liderazgo para la gestión de equipos de alto desempeño", "curso": "LDR", "clave": "55700", "créditos": 6},
        ],
        "Planeación y Estrategia": [
            {"materia": "Simulación de negocios", "curso": "ADM", "clave": "55702", "créditos": 6},
            {"materia": "Visión estratégica de la tecnología", "curso": "ADM", "clave": "55704", "créditos": 6},
        ],
        "**Ciencia de Datos e Inteligencia Artificial (Seleccionar al menos 2 materias)":[
            {"materia": "Inteligencia Artificial*",  "curso": "ITI", "clave": "55701", "créditos": 6},
            {"materia": "Machine learning*",  "curso": "ITI", "clave": "55703", "créditos": 6},
            {"materia": "Blockchain", "curso": "ITI", "clave": "55706", "créditos": 6},
            {"materia": "Internet de las cosas", "curso": "ITI", "clave": "55702", "créditos": 6},
            {"materia": "Realidad virtual y aumentada", "curso": "ITI", "clave": "55705", "créditos": 6},
        ],
        "Análisis e Inteligencia de Negocios": [
            {"materia": "Herramientas de Inteligencia de Negocios*", "curso": "ADM", "clave": "55706", "créditos": 6},
            {"materia": "Modelado y visualización de datos*", "curso": "MAT", "clave": "55706", "créditos": 6},
            {"materia": "Modelos y herramientas de Analítica de datos aplicada a los negocios*",  "curso": "MAT", "clave": "55707", "créditos": 7},
            {"materia": "Administración de riesgos de Negocio", "curso": "ADM", "clave": "55705", "créditos": 6},
            {"materia": "Sistemas Estratégicos de Dirección y Evaluación de Desempeño", "curso": "ADM", "clave": "55707", "créditos": 6},
            
        ],

        "Ingeniería y Operaciones": [
            {"materia": "Lean Management*",  "curso": "IIND", "clave": "55701", "créditos": 7},
            {"materia": "Sistemas de gestión empresarial*", "curso": "IIND", "clave": "55703", "créditos": 6},
            {"materia": "Six sigma*", "curso": "IIND", "clave": "55705", "créditos": 6},
            {"materia": "Dirección de operaciones en Empresas", "curso": "IIND", "clave": "55700", "créditos": 6},
            {"materia": "Logística y cadena de suministros", "curso": "IIND", "clave": "55702", "créditos": 6},
            {"materia": "Sistemas flexibles de Manufactura", "curso": "IIND", "clave": "55704", "créditos": 6},
        ],
            
        "Seminarios y Tesis":[
            {"materia": "Proyecto integrador", "curso": "INV", "clave": "55700", "créditos": 7},
            {"materia": "Temas multidisciplinarios de vanguardia", "curso": "CUL", "clave": "55700", "créditos": 6},
            {"materia": "Temas selectos multidisciplinarios", "curso": "CUL", "clave": "55701", "créditos": 6},
            {"materia": "Temas Selectos sobre Género", "curso": "CUL", "clave": "55702", "créditos": 6},
            {"materia": "Temas Selectos sobre vulnerabilidad, discriminación y equidad", "curso": "CUL", "clave": "55703", "créditos": 6},
            {"materia": "Tesis de maestría", "curso": "INV", "clave": "55701", "créditos": 7},
        ],

        "Innovación Tecnológica y Emprendimiento":[
            {"materia": "Administración de proyectos*", "curso": "EMP", "clave": "55700", "créditos": 6},
            {"materia": "Desing Thinking*", "curso": "EMP", "clave": "55701", "créditos": 7},
            {"materia": "Emprendimiento de negocios", "curso": "EMP", "clave": "55702", "créditos": 6},
            {"materia": "Mindset digital",  "curso": "EMP", "clave": "55703", "créditos": 7},
            {"materia": "Negocios electrónicos", "curso": "EMP", "clave": "55704", "créditos": 6},
        ],
        "Economía y Finanzas": [
            {"materia": "Empresas, clústeres, desarrollo económico y social**", "curso": "FIN", "clave": "55701", "créditos": 7},
            {"materia": "Finanzas bursátiles y digitales*", "curso": "FIN", "clave": "55702", "créditos": 6},
            {"materia": "Fundamentos analíticos para finanzas*", "curso": "FIN", "clave": "55704", "créditos": 7},
            {"materia": "Portafolios de inversión*", "curso": "FIN", "clave": "55705", "créditos": 6},
        ],
        "Mercadotecnia":[
            {"materia": "Comercio electrónico y estrategias de mercadotecnia digital*", "curso": "MER", "clave": "55701", "créditos": 6}, 
            {"materia": "Análisis de mercado y toma de decisiones", "curso": "MER", "clave": "55700", "créditos": 6},
            {"materia": "Estrategias de mercadotecnia", "curso": "MER", "clave": "55702", "créditos": 7},
            {"materia": "Inteligencia y perspectiva estratégica del consumidor",  "curso": "MER", "clave": "55704", "créditos": 6},        
        ],

        "Toma de Decisiones":[
            {"materia": "Análisis de datos multivariante", "curso": "MAT", "clave": "55700", "créditos": 6},
            {"materia": "Herramientas de análisis de decisiones", "curso": "MAT", "clave": "55703", "créditos": 7},
            {"materia": "Estadística Avanzada", "curso": "MAT", "clave": "55708", "créditos": 6},
            {"materia": "Estadística descriptiva e inferencial", "curso": "MAT", "clave": "55702", "créditos": 6},
        ],
        "Comunicación":[
            {"materia": "Comunicación digital*", "curso": "COM", "clave": "55701", "créditos": 6},
            {"materia": "Gestión estratégica de la comunicación", "curso": "COM", "clave": "55702", "créditos": 7},
        ],
        "Talento Humano y Organizacional":[
            {"materia": "Consultoría y desarrollo organizacional*", "curso": "PSI", "clave": "55702", "créditos": 7},
            {"materia": "Gestión integral del talento*", "curso": "PSI", "clave": "55704", "créditos": 7},
        ]
    }

    materias_obligatorias = [
        {"materia": "Liderazgo de Acción Positiva", "curso": "LDR", "clave": "55703", "créditos": 6},
        {"materia": "Planeación Estratégica de las organizaciones", "curso": "ADM", "clave": "55701", "créditos": 7},
        {"materia": "Ciencia de Datos", "curso": "ITI", "clave": "55700", "créditos": 7},
        {"materia": "Minería de datos", "curso": "ITI", "clave": "55704", "créditos": 7},
    ]

    # Función para obtener detalles completos de cada materia
    def get_materia_details(materia_nombre):
        # Buscar en áreas de competencia
        for area, materias in areas_competencias.items():
            for materia in materias:
                if materia["materia"] == materia_nombre:
                    return {
                        "curso_clave": f"{materia['curso']}{materia['clave']}",
                        "curso": materia["curso"],
                        "clave": materia["clave"],
                        "nombre_materia": f"{materia['materia']}",
                        "creditos": materia["créditos"]
                    }
        
        # Buscar en materias obligatorias
        for materia in materias_obligatorias:
            if materia["materia"] == materia_nombre:
                return {
                    "curso_clave": f"{materia['curso']}{materia['clave']}",
                    "curso": materia["curso"],
                    "clave": materia["clave"],
                    "nombre_materia": f"{materia['materia']}",
                    "creditos": materia["créditos"]
                }
        return None

    # Función para calcular créditos totales
    def calcular_creditos_totales(materias_seleccionadas):
        creditos = 0
        for materia_nombre in materias_seleccionadas:
            detalles = get_materia_details(materia_nombre)
            if detalles:
                creditos += detalles["creditos"]
        return creditos

    # Interfaz de usuario
    st.title("Formulario de Registro de Materias")

    with st.form("registro_form"):
        # Información personal
        st.header("Datos Personales")
        nombre = st.text_input("Nombre completo:")
        identificacion = st.text_input("ID:")
        telefono = st.text_input("Teléfono:")
        correo = st.text_input("Correo electrónico:")
        genero = st.radio("Género:", ["Masculino", "Femenino", "Otro", "Prefiero no decir"])
        
        # Selección de materias
        st.header("Selección de Materias:")
        st.write("## Programa: Big data e Inteligencia artificial")
        st.write("")
        st.write("## Consideraciones para el llenado del formulario:")
        st.write(""" 
        ##### - ***Debes seleccionar al menos 2 materias*** del área de Ciencia de datos e Inteligencia Artificial
        ##### - Recuerda seleccionar un ***máximo*** de 9 materias (58 créditos)
        ##### - Las materias obligatorias (Liderazgo de acción positiva, Planeación Estratégica de las organizaciones, Ciencia de Datos, Minería de datos) ya se encuentran ***precargadas*** (27 créditos)
        ##### - Materias que en su contenido abonan para examen de certificación, tendrán un * al lado de su nombre
        ##### - [En este enlace podrás consultar las certificaciones a las que abonan las materias](https://drive.google.com/file/d/1GNkweJmmwMd4CWEKf8KsGybZpb-3bnhJ/view?usp=sharing)
        ##### - Al presionar el botón de Enviar Registro, ***por favor espera un poco***, aparecerá un botón para descargar tu formulario en PDF para su consulta
        ##### - [En este enlace podrás consultar el contenido de cada materia](https://drive.google.com/file/d/1Er48k2mOYuBzQDmDGmzXNH-Y_byWd7tj/view?usp=sharing)
        """)
        st.write("")
        st.write("")
        st.write("## Áreas de competencia:")
        opciones_seleccionadas = []
        
        for area, materias in areas_competencias.items():
            with st.expander(f" ***{area}***", expanded=False):
                st.write("")
                for materia in materias:
                    st.write("---")  # Línea divisoria entre materias
                    if st.checkbox(f"{materia['materia']} (Créditos: {materia['créditos']})"):
                        opciones_seleccionadas.append(materia["materia"])
                        
        
        submitted = st.form_submit_button("Enviar Registro")

        if submitted:
            # Validaciones
            if not all([nombre, telefono, correo]):
                st.error("Por favor, complete todos los campos obligatorios.")
            else:
                # Añadir materias obligatorias
                materias_con_obligatorias = opciones_seleccionadas.copy()
                for materia in materias_obligatorias:
                    if materia["materia"] not in materias_con_obligatorias:
                        materias_con_obligatorias.append(materia["materia"])
                
                # Validar materias de Ciencia de Datos
                materias_ciencia_datos = [
                    "Inteligencia Artificial*", "Machine learning*", "Blockchain",
                    "Internet de las cosas", "Realidad virtual y aumentada"
                ]
                seleccionadas_ciencia_datos = [m for m in materias_con_obligatorias if m in materias_ciencia_datos]
                
                if len(seleccionadas_ciencia_datos) < 2:
                    st.error("Debes seleccionar al menos 2 materias del área 'Ciencia de Datos e Inteligencia Artificial'.")
                else:
                    # Validar número máximo de materias (9) y créditos (85)
                    total_materias = len(materias_con_obligatorias)
                    total_materias2 = total_materias - 4
                    creditos_totales = calcular_creditos_totales(materias_con_obligatorias)
                    
                    if total_materias > 13:
                        st.error(f"Has seleccionado {total_materias2} materias. El máximo permitido es 9.")
                    elif creditos_totales > 85:
                        st.error(f"Total de créditos: {creditos_totales}. El límite permitido es 85 créditos.")
                    elif creditos_totales < 76:
                        st.error(f"Total de créditos: {creditos_totales}. El mínimo permitido es 76 créditos.")
                    else:
                        # Preparar filas para Google Sheets (una por materia)
                        rows_to_save = []
                        timestamp = datetime.now().strftime("%Y-%m-%d")
                        programa = "Big data e Inteligencia Artificial"
                        
                        for materia_nombre in materias_con_obligatorias:
                            detalles = get_materia_details(materia_nombre)
                            if detalles:
                                row = [
                                    programa,
                                    identificacion,
                                    nombre,
                                    f"{detalles['curso']}{detalles['clave']} - {detalles['nombre_materia']}",
                                    detalles["creditos"],
                                    f"{detalles['curso']}{detalles['clave']}",
                                    detalles["clave"],
                                    detalles["nombre_materia"],
                                    timestamp,
                                    telefono,
                                    correo,
                                    genero
                                ]
                                rows_to_save.append(row)
                        
                        # Guardar en Google Sheets
                        if save_to_gsheets(rows_to_save):
                            st.success(f"¡Registro exitoso! Se guardaron {len(rows_to_save)} materias.")
                            st.info(f"Total de créditos: {creditos_totales}")
                            # Almacenar datos y activar bandera para mostrar el botón
                            st.session_state.download_data = rows_to_save
                            st.session_state.show_download = True
                        else:
                            st.error("Error al guardar en la base de datos. Por favor, intente nuevamente.")

    # Fuera del formulario - Botón de descarga (MODIFICADO PARA PDF)
    if st.session_state.download_data:
        # Crear DataFrame con los datos
        df = pd.DataFrame(st.session_state.download_data, columns=[
            "Programa", "ID", "Nombre", "Materia",
            "Créditos", "Curso", "Clave", "Nombre de la Materia",
            "Timestamp", "Teléfono", "Correo", "Género"
        ])
        
        # Obtener datos para el PDF
        nombre = df.iloc[0]['Nombre']
        programa = df.iloc[0]['Programa']
        materias = df[['Nombre de la Materia', 'Créditos']]
        creditos_totales = df['Créditos'].sum()
        
        # Crear PDF en memoria
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []

        # --- ENCABEZADO SIMPLIFICADO ---
        # Espacio antes de la imagen
        elements.append(Spacer(1, 1))
    
        # Agregar imagen de encabezado (centrada)
        try:
            img = Image("encabezado.jpg", width=1.5*inch, height=1.8*inch)
            img.hAlign = 'CENTER'  # Centrar la imagen
            elements.append(img)
        except:
            st.warning("No se pudo cargar la imagen de encabezado")
    
        # Espacio después de la imagen
        elements.append(Spacer(1, 24))
            
        
        # Estilos
        styles = getSampleStyleSheet()
        style_normal = styles['Normal']
        style_heading = styles['Heading1']
        
        # Mensaje de bienvenida
        welcome_msg = f"Estimado {nombre}, bienvenido a tu programa de Maestría en {programa}."
        elements.append(Paragraph(welcome_msg, style_heading))
        elements.append(Spacer(1, 12))
        
        # Texto descriptivo
        elements.append(Paragraph("A continuación compartimos contigo el programa ideal que has generado:", style_normal))
        elements.append(Spacer(1, 24))
        
        # Crear tabla con materias
        table_data = [['Nombre de la Materia', 'Créditos']]  # Encabezados
        
        for _, row in materias.iterrows():
            table_data.append([row['Nombre de la Materia'], str(row['Créditos'])])
        
        # Añadir fila de totales
        table_data.append(['Créditos totales', f'{creditos_totales}'])
        
        # Crear y estilizar tabla
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 24))
         # --- AGREGAR PIE DE PÁGINA CON IMAGEN ---
        def add_footer(canvas, doc):
            # Ruta a tu imagen de pie de página
            footer_img_path = "footer.png"  # o "footer.png"
            try:
                footer_img = ImageReader(footer_img_path)
                # Posicionar en la parte inferior (x, y, width, height)
                canvas.drawImage(footer_img, 1.3*inch, 0.5*inch, width=6*inch, height=0.75*inch)
            except:
                pass  # Silenciar error si no se encuentra la imagen

        # Construir PDF
        doc.build(elements, onFirstPage=add_footer, onLaterPages=add_footer)
        
        # Configurar el botón de descarga para PDF
        st.download_button(
            label="Descargar a PDF",
            data=buffer.getvalue(),
            file_name="Programa_Maestria.pdf",
            mime="application/pdf"
        )
