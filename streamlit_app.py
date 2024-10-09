import base64

import pandas as pd
import streamlit as st

import base_datos
import bingo
import esta_partida

st.set_page_config(layout="wide")

# Cargar el archivo de Excel
qa_df = pd.read_excel("content/QA.xlsx")

# Inicializar variables en session_state si no existen
st.session_state.setdefault("preguntas_restantes", qa_df["Pregunta"].tolist())
st.session_state.setdefault("preguntas_mostradas", [])

# Función para añadir el fondo
def set_background(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
        }}
        /* Barra superior (Deploy) transparente */
        header {{
            background: transparent !important;
        }}
        /* Ocultar el menú de navegación predeterminado si existe */
        [data-testid="stSidebarNav"] {{
            display: none;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Llamar a la función para establecer el fondo
set_background("content/Background.png")

# Inicializar la opción de menú por defecto si no existe en session_state
if "menu_option" not in st.session_state:
    st.session_state.menu_option = "Bingo"  # Set Bingo as the default tab

# Crear el menú en la barra lateral derecha con iconos y texto personalizados
with st.sidebar:
    st.sidebar.markdown("<h1>Menú</h1>", unsafe_allow_html=True)

    st.markdown(
        """
    <style>
        [data-testid=stSidebar] {
            background-color: #ffffff50;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    # Simulación del menú con columnas
    col1, col2 = st.columns([1, 6])
    with col1:
        st.image("content/play.png", width=30)
    with col2:
        if st.button("Bingo"):
            st.session_state.menu_option = "Bingo"

    col3, col4 = st.columns([1, 6])
    with col3:
        st.image("content/pause.png", width=30)
    with col4:
        if st.button("Esta partida"):
            st.session_state.menu_option = "Esta partida"

    col5, col6 = st.columns([1, 6])
    with col5:
        st.image("content/database.png", width=30)
    with col6:
        if st.button("Base de datos"):
            st.session_state.menu_option = "Base de datos"

# Mostrar el contenido basado en la pestaña seleccionada
if st.session_state.menu_option == "Bingo":
    bingo.show()
elif st.session_state.menu_option == "Esta partida":
    esta_partida.show()
elif st.session_state.menu_option == "Base de datos":
    base_datos.show()
