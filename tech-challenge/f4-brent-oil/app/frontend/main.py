import streamlit as st
from . import blocks

def setup():
    st.set_page_config(
        page_title="Hello World",
        page_icon="🧊",
        layout="centered",
        initial_sidebar_state="auto",
    )


def app_streamlit():
    setup()
    blocks.header()
    st.divider()
    blocks.dash()
    #dash, history, content = st.tabs(["Previsão", "Histórico", "Modelos"])
#
    #with dash:
    #    blocks.dash()
#
    #with history:
    #    blocks.hist()
#
    #with content:
    #    blocks.contet()



