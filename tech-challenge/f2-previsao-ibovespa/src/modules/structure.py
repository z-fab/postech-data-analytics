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


def indicators_ibovespa() -> None:

    last_date = getDataIbov()[1]

    data = getConsolidate(90)
    data = data[data['close'] > 0]

    mae = round(np.mean(np.abs(data['diff'])))
    mape = round(np.abs(data['diff'] / data['close']).mean()*100,2)

    cols = st.columns(3)

    cols[0].metric(
        label=":gray[Última atualização]", 
        value=last_date.strftime('%d/%m/%Y')
    )
    cols[1].metric(
        label=f":green[MAE] (Mean Absolute Error) - Últimos 90 Dias", 
        value=f"± {mae} pts"
    )
    cols[2].metric(
        label=f":green[MAPE] (Mean Absolute Percent Error) - Últimos 90 Dias", 
        value= f"{mape}%"
    )