import os
import datetime
import numpy as np
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

from .database import Database

@st.cache_data
def getDataIbov(delta=365) -> pd.DataFrame:
    db = Database(path = os.path.join(os.getenv('DATA_DIR'), 'ibovespa.db'))
    df = db.getDataIbov(start_date=datetime.datetime.now().date()-datetime.timedelta(days=delta))
    return (pd.DataFrame(df), db.getLastDateIbov())

@st.cache_data
def getPredict() -> pd.DataFrame:
    db = Database(path = os.path.join(os.getenv('DATA_DIR'), 'ibovespa.db'))
    df = db.getDataPred()
    return (pd.DataFrame(df), db.getLastDatePred())

def getConsolidate(delta=14) -> pd.DataFrame:
    db = Database(path = os.path.join(os.getenv('DATA_DIR'), 'ibovespa.db'))
    df = db.getDataConsolidate(h = delta)
    return pd.DataFrame(df)



def header() -> None:
    st.markdown("# Tech Challenge: :blue[Previsão IBovespa]")
    st.markdown(
        ":gray[Tech Challenge é o projeto final de fase da **PósTech**, ele engloba os conhecimentos obtidos em todas as disciplinas vistas até aquele momento.]"
    )
    st.markdown(
        """
        **Contexto:**
          Imagine que você foi escalado para um time de investimentos e precisará realizar um modelo preditivo com dados da IBOVESPA (Bolsa de valores) para criar uma série temporal e prever diariamente o fechamento da base.
    """
    )

def graph_pred(delta = 14, title = "") -> None:

    pred = getPredict()[0][-delta:]
    pred['date'] = pd.to_datetime(pred['date'])
    pred.set_index('date', inplace=True)

    ibov = getDataIbov()[0][['date', 'close']]
    ibov['date'] = pd.to_datetime(ibov['date'])
    ibov.set_index('date', inplace=True)
    ibov = ibov.resample('D').ffill().reset_index()

    df = pred.merge(ibov, on='date', how='left')
    df.rename(columns={'close': 'IBov', 'predict': 'Predição'}, inplace=True)
    df = df.melt(id_vars=['date'], value_vars=['IBov', 'Predição'])

    min_close = df['value'].min() * .93
    max_close = df['value'].max() * 1.03

    fig = px.area(df, x='date', y='value', color='variable', title=title, color_discrete_map={'IBov': '#457b9d', 'Predição': '#e63946'})

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeslider_bgcolor='white',
        rangeslider_thickness=0.18,
    )

    fig.update_traces(stackgroup = None, fill = 'tozeroy')

    fig.update_yaxes(rangemode="normal")

    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Pontos",
        legend_title="IBovespa",
        yaxis_range=[min_close, max_close],
        legend_title_text='Índices'

    )

    st.plotly_chart(fig, use_container_width=True)

def table_ibovespa() -> None:

    pred = getPredict()[0][-90:]
    pred['date'] = pd.to_datetime(pred['date'])
    pred.set_index('date', inplace=True)

    ibov = getDataIbov()[0][['date', 'close']]
    ibov['date'] = pd.to_datetime(ibov['date'])
    ibov.set_index('date', inplace=True)
    ibov = ibov.resample('D').ffill().reset_index()

    df = pred.merge(ibov, on='date', how='left').reset_index(drop=True)

    df_final = df.sort_values(by='date', ascending=False)
    df_final['date'] = pd.to_datetime(df_final['date']).dt.strftime('%d/%m/%Y')
    df_final['predict'] = df_final['predict'].round(0).astype(int)
    df_final['close'] = df_final['close'].fillna(0).astype(int)
    df_final['diff'] = df_final['close'] - df_final['predict']
    df_final['diff_percent'] = round((df_final['diff'] / df_final['close']) * 100,1)
    df_final.set_index('date', inplace=True)

    df_final[['close', 'predict', 'diff_percent', 'diff']] = df_final[['close', 'predict', 'diff_percent', 'diff']].astype(str)

    df_final['predict'] = df_final['predict'].apply(lambda x: '-' if x == '0' else f"{x} pts.")
    df_final['close'] = df_final['close'].apply(lambda x: '-' if x == '0' else f"{x} pts.")
    df_final['diff_percent'] = df_final[['close', 'diff_percent']].apply(lambda x: '-' if x['close'] == '-' else f"{x['diff_percent']}%", axis=1)
    df_final['diff'] = df_final[['close', 'diff']].apply(lambda x: '-' if x['close'] == '-' else f"{x['diff']} pts.", axis=1)
    
    df_final = (
        df_final
        .rename(columns={'close': 'Pontuação', 'predict': 'Previsão', 'date': 'Data', 'diff': 'Diferença (pontos)', 'diff_percent': 'Diferença (%)'})
    )
    
    st.dataframe(df_final[['Pontuação', 'Previsão', 'Diferença (pontos)', 'Diferença (%)']], use_container_width=True)


def indicators_ibovespa():

    last_date = getDataIbov()[1]

    data = getConsolidate(30)
    data = data[data['close'] > 0]

    mae = round(np.mean(np.abs(data['diff'])))
    mape = round(np.abs(data['diff'] / data['close']).mean()*100,2)

    cols = st.columns(3)

    cols[0].metric(
        label=":gray[Última atualização IBovespa]", 
        value=last_date.strftime('%d/%m/%Y')
    )
    cols[1].metric(
        label=f":green[MAE] (Mean Absolute Error) - Últimos 30 Dias", 
        value=f"± {mae} pts"
    )
    cols[2].metric(
        label=f":green[MAPE] (Mean Absolute Percent Error) - Últimos 30 Dias", 
        value= f"{mape}%"
    )

def desc_project():

    st.info('Para ver o conteúdo completo e o código do Dashboard acesse o repositório do projeto em https://github.com/z-fab/postech-data-analytics/tree/master/tech-challenge/f2-previsao-ibovespa', icon="ℹ️")
    st.markdown('<br>', unsafe_allow_html=True)

    content = f'''

        Este projeto faz parte do módulo de Data Analytics da pós-graduação da POSTECH FIAP, visando desenvolver um modelo preditivo para o fechamento diário do índice IBOVESPA.

        O problema fornecido foi: Imagine que você foi escalado para um time de investimentos e precisará realizar um **modelo preditivo** com dados da **IBOVESPA** (Bolsa de valores) para criar uma série temporal e prever diariamente o fechamento da base.

        Dado a característica estocástica do mercado financeiro, a previsão de fechamento da IBOVESPA é um problema _complexo e de difícil solução_, por isso o objetivo será criar um modelo de previsão de fechamento da IBOVESPA apenas para os 3 dias seguintes. A previsão será feita com base nos dados históricos de fechamento.

        Como meta, o modelo deve ter um **erro médio percentual absoluto (MAPE) menor que 2%** para os próximos 3 dias.

        ## Metodologia

        Os dados serão coletados via API do Yahoo Finance utilizando o pacote `yfinance`. Os dados serão coletados e atualizados em um Banco de Dados Local (SQLite) todos os dias as 06:00.

        Em alguns casos a API do Yahoo Finance não retorna os dados do dia anterior, por isso, caso isso ocorra, podemos ter uma defasaem de 1 dia nos dados.

        ## Modelos Testados

        Para a resolução do problema foram testados 3 modelos e comparados com o resultado de um modelo de Baseline (Naive):

        - ARIMA
        - SARIMA / SARIMAX
        - XGBoost

        Como baseline foi escolhido o modelo Naive que utiliza uma média móvel de 7 dias para prever os próximos 3 dias.

        ## Conclusão

        O modelo SARIMA treinando com os 180 dias anteriores foi o escolhido. Esse modelo demonstrou um bom resultado (tanto na validação quanto no teste) e por isso criamos o Dashboard e o sistema de predição automática com ele.

        ### Dashboard

        O Dashboard foi criado utilizando o Streamlit. Existe uma rotina que atualiza diariamente os dados e, quando necessário, realiza a previsão para os próximos 3 dias.

    '''

    st.markdown(content, unsafe_allow_html=True)