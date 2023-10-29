import streamlit as st

from classes import graphs as g
from classes import structure as s
from classes import functions as f


if __name__ == "__main__":
    f.config_streamlit()
    df = f.load_data()
    s.header()

    tabs = st.tabs(["🌎 Introdução", "📋 Tabela", "📊 Gráficos"])

    with tabs[0]:
        s.tab_intro(df)

    with tabs[1]:
        s.tab_tabela(df)

    with tabs[2]:
        s.tab_graph(df)
