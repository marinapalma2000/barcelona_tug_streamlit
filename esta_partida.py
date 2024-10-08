import pandas as pd
import streamlit as st

# Cargar el archivo de Excel
qa_df = pd.read_excel("content/QA.xlsx")

# Inicializar las preguntas mostradas si no existen
if "preguntas_mostradas" not in st.session_state:
    st.session_state.preguntas_mostradas = []

if "indice_carrusel" not in st.session_state:
    st.session_state.indice_carrusel = 0


def show():
    st.markdown('<h3 class="tab-title">Preguntas mostradas en esta partida</h3>', unsafe_allow_html=True)

    # Crear sub-pestañas dentro de "Esta partida"
    sub_selection = st.radio("", ["Solo preguntas", "Preguntas y respuestas"])

    if sub_selection == "Solo preguntas":
        st.write("Estas son las preguntas que ya han salido en esta partida:")
        if st.session_state.preguntas_mostradas:
            preguntas_mostradas_df = pd.DataFrame(st.session_state.preguntas_mostradas, columns=["Preguntas"])
            st.table(preguntas_mostradas_df)
        else:
            st.write("Aún no se ha mostrado ninguna pregunta.")

    elif sub_selection == "Preguntas y respuestas":
        st.write("Preguntas y respuestas:")

        # Mostrar las preguntas y respuestas en formato carrusel
        if st.session_state.preguntas_mostradas:
            # Obtener la pregunta actual
            current_question = st.session_state.preguntas_mostradas[st.session_state.indice_carrusel]
            # Obtener la respuesta correspondiente
            current_answer = qa_df[qa_df["Pregunta"] == current_question]["Respuesta"].values[0]

            # Mostrar la pregunta y respuesta con texto más grande
            st.markdown(
                f"""
                <div style="font-size:40px; font-weight:bold; color:#11003e; margin-bottom:20px; text-align:center;">
                    Pregunta: {current_question}
                </div>
                <div style="font-size:40px; color:#333333; text-align:center;">
                    Respuesta: {current_answer}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Controles para el carrusel
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                if st.button("Anterior", key="prev"):
                    st.session_state.indice_carrusel = (st.session_state.indice_carrusel - 1) % len(
                        st.session_state.preguntas_mostradas
                    )
            with col3:
                if st.button("Siguiente", key="next"):
                    st.session_state.indice_carrusel = (st.session_state.indice_carrusel + 1) % len(
                        st.session_state.preguntas_mostradas
                    )
        else:
            st.write("Aún no se ha mostrado ninguna pregunta.")
