import streamlit as st
from . import controller as ctrl


def dash():
    st.markdown(" ")
    ctrl.get_next_prediction()
    st.divider()
    ctrl.get_prediction_graph()
    st.divider()
    ctrl.get_table_predictions()


def hist():
    ctrl.get_history_graph()

def contet():
    pass

def header():
    st.markdown("# Tech Challenge: :red[Petróleo Brent]")
    st.markdown(
        ":gray-background[Tech Challenge] é o projeto final de fase da **PósTech**, ele engloba os conhecimentos obtidos em todas as disciplinas vistas até aquele momento."
    )
    st.markdown(
        """
        **Contexto:**
          Imagine que você foi escalado para um time de investimentos e precisará realizar um modelo preditivo com dados da IBOVESPA (Bolsa de valores) para criar uma série temporal e prever diariamente o fechamento da base.
    """
    )