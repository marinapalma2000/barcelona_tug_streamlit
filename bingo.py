import random
import time

import pandas as pd
import streamlit as st

# Cargar el archivo de Excel
qa_df = pd.read_excel("content/QA.xlsx")

# Inicializar variables en session_state si no existen
st.session_state.setdefault("preguntas_restantes", qa_df["Pregunta"].tolist())
st.session_state.setdefault("preguntas_mostradas", [])


def generar_pregunta():
    if st.session_state.preguntas_restantes:
        pregunta = random.choice(st.session_state.preguntas_restantes)
        st.session_state.preguntas_restantes.remove(pregunta)
        st.session_state.preguntas_mostradas.append(pregunta)

        # Mostrar imagen en lugar de pregunta si es "Astro", "Einstein", o "Datafam"
        if pregunta == "Astro":
            return "image", "content/Astro.png"
        elif pregunta == "Einstein":
            return "image", "content/Einstein.png"
        elif pregunta == "Datafam":
            return "image", "content/Datafam.png"
        else:
            return "text", pregunta
    else:
        return "text", "¡No quedan más preguntas!"


def show():
    # Añadir animaciones CSS para desvanecimiento y estilo para el contador
    st.markdown(
        """
        <style>
        .fade-in {
            opacity: 0;
            animation: fadeIn ease 2s;
            animation-fill-mode: forwards;
        }

        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }

        /* Estilo para el contador en la esquina superior derecha, ajustado para no superponerse */
        .contador {
            position: fixed;
            top: 50px;  /* Ajustado para que esté más abajo */
            right: 10px;
            font-size: 24px;
            color: #FF5733;
            background-color: #ffffff;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Mostrar la imagen en la parte superior
    st.image("content/bingo_title.png", width=500)

    # Botón para mostrar pregunta o imagen
    if st.button("Generar pregunta"):
        # Generar la pregunta o imagen inmediatamente
        tipo, contenido = generar_pregunta()

        # Mostrar la pregunta o imagen de inmediato
        if tipo == "image":
            if contenido == "content/Datafam.png":
                width = 500
            else:
                width = 300

            # Centrar la imagen usando columnas con animación de desvanecimiento
            col1, col2, col3 = st.columns([2, 2, 2])  # Columnas para centrar la imagen
            with col2:
                st.image(contenido, width=width)  # Mostrar la imagen con fade-in aplicado

        else:
            # Mostrar el texto de la pregunta con animación de desvanecimiento
            st.markdown(
                f"""
                <p class="fade-in" style="font-size:50px; color:#11003e; font-weight: bold; font-family:'baskerville'; text-align:center; 
                    margin-top:40px;">
                    {contenido}
                </p>
                """,
                unsafe_allow_html=True,
            )

        # Crear el temporizador después de que la pregunta se muestre
        countdown_placeholder = st.empty()

        # Realizar la cuenta atrás de 15 segundos
        for i in range(15, 0, -1):
            countdown_placeholder.markdown(
                f'<div class="contador">Tiempo restante: {i} segundos</div>', unsafe_allow_html=True
            )
            time.sleep(1)

        # Limpiar el espacio del contador después de la cuenta atrás
        countdown_placeholder.empty()

    else:
        st.write("Pulsa el botón para iniciar el juego.")
