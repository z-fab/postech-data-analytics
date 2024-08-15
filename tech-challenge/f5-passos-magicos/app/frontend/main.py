import streamlit as st
from frontend import blocks
from backend.data_process import load_data, get_alunos


def setup():
    st.set_page_config(
        page_title="Passos Mágicos - Presença Alunos",
        page_icon="📚",
        layout="centered",
        initial_sidebar_state="collapsed",
    )


def app_streamlit():
    setup()
    data = load_data()
    df_aluno = get_alunos()
    blocks.header()

    pred, info = st.tabs(["🔍 Previsão", "📚 Informações"])

    with info:
        blocks.info(data)

    with pred:
        blocks.prev(df_aluno, data)
