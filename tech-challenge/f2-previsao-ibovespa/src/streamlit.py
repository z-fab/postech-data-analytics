import logging
import os
import streamlit as st
from modules import structure as struct

# Definindo variáveis de ambiente com os caminhos dos diretórios
PATHS = {}
PATHS['SRC_DIR'] = os.path.dirname(__file__)
PATHS['BASE_DIR'] = os.path.dirname(PATHS['SRC_DIR'])
PATHS['DATA_DIR'] = os.path.join(PATHS['BASE_DIR'], 'data')
PATHS['LOG_DIR'] = os.path.join(PATHS['BASE_DIR'], 'log')

for key, value in PATHS.items():
    os.environ[key] = value


st.set_page_config(
    page_title="Tech Challenge: Previsão IBovespa",
    page_icon=":chart_with_upwards_trend:",
    layout="wide"
)

struct.header()
st.divider()
struct.indicators_ibovespa()
st.divider()

struct.graph_pred(365, title="IBovespa - Fechado e Previsão")

struct.table_ibovespa()