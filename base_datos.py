import pandas as pd
import streamlit as st

# Cargar el archivo de Excel
qa_df = pd.read_excel("content/QA.xlsx")


def show():
    st.markdown('<h3 class="tab-title">Base de Datos de Preguntas y Respuestas</h3>', unsafe_allow_html=True)

    # Mostrar la base de datos completa
    st.write("Aquí puedes ver todas las preguntas y respuestas del archivo QA.xlsx:")
    st.dataframe(qa_df)
