from services import Database
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

db = Database()


def get_history_graph():
    # Primeiro, vamos converter o índice para datetime, se necessário
    df_brent_oil = pd.DataFrame(db.get_all_brent_oil(), columns=['id', 'date', 'close', 'open', 'high', 'low', 'volume'])

    # Criando o gráfico de linha para a série temporal
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df_brent_oil['date'], y=df_brent_oil['close'], mode='lines', name='Preço do Petróleo Brent'))

    # Adicionando eventos significativos como círculos numerados
    events = {
        '2008-09-15': 'Crise Financeira Global',
        '2011-03-01': 'Primavera Árabe',
        '2014-11-27': 'OPEP não corta produção, preço cai',
        '2016-01-01': 'Acordo de Corte da OPEP',
        '2018-05-08': 'EUA saem do acordo nuclear com Irã',
        '2020-03-01': 'Pandemia de COVID-19',
        '2020-04-20': 'Preços do WTI negativos',
        '2022-02-24': 'Invasão da Ucrânia pela Rússia',
        '2023-02-01': 'Tensões no Oriente Médio'
    }

    # Numerar os eventos para colocar dentro dos círculos
    for i, (date, event) in enumerate(events.items(), 1):
        close_price = df_brent_oil.where(df_brent_oil['date'] == date)['close'].values[0]
        offset_price = 155  # Ajuste este valor conforme necessário

        fig.add_trace(go.Scatter(
            x=[date, date],
            y=[close_price, offset_price],
            mode='lines',
            line=dict(color='blue', dash='dash'),
            showlegend=False
        ))

        # Adiciona o marcador numerado
        fig.add_trace(go.Scatter(
            x=[date],
            y=[offset_price],
            mode='markers+text',
            marker=dict(size=20, color='blue'),
            text=str(i),
            textposition='middle center',
            textfont=dict(color='white', size=10),
            showlegend=False
        ))

            # Adiciona uma linha tracejada conectando o marcador à série temporal


    # Configurando o layout do gráfico
    fig.update_layout(
        title='Preço Histórico do Petróleo Brent com Eventos Importantes (Numerados)',
        xaxis_title='Data',
        yaxis_title='Preço de Fechamento (USD)',
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    # Mostrar o gráfico
    st.plotly_chart(fig)


def get_predictions():
    df = pd.DataFrame(db.get_all_brent_prediciton(), columns=['id', 'date', 'close', 'open', 'high', 'low', 'volume', 'id_pred', 'value', 'model']).sort_values('date', ascending=True)
    df.drop(columns=['id_pred', 'open', 'high', 'low', 'volume'], inplace=True)
    df['Data'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
    df['Fechamento'] = df['close']
    df['Previsão'] = df['value'].round(2)
    df['Diferença'] = df['Previsão'] - df['Fechamento']
    df['Modelo'] = df['model'].apply({
        'meta': 'Meta-Modelo',
        'knn': 'KNN',
        'svm': 'SVM', 
        'xgb': 'XGBoost', 
        'br': 'Bayesian Ridge',
        'mlp': 'Multi Layer Perceptron'}.get)

    df.drop(columns=['date', 'close', 'value', 'model'], inplace=True)
    return df.sort_values('Data', ascending=False).set_index('id')

def get_prediction_graph():

    all_models = st.toggle("Ver Média de todos os Modelos")
    model_selected = st.multiselect(
        "Qual previsão você deseja visualizar?",
        ["Meta-Modelo", "KNN", "SVM", "XGBoost", "Bayesian Ridge", "Multi Layer Perceptron"],
        ["Meta-Modelo"],
        disabled=all_models
    )
    
    df = get_predictions()
    fig = go.Figure()

    if all_models:
        df_aux = df[['Data', "Fechamento", 'Previsão']].groupby('Data').mean().reset_index()
        
        fig.add_trace(
            go.Scatter(
                y=df_aux['Fechamento'], x=df_aux['Data'], mode='lines', name='Fechamento'
            )
        )
        fig.add_trace(
            go.Scatter(
                y=df_aux['Previsão'], x=df_aux['Data'], mode='lines', name='Previsão'
            )
        )

    else:
        fig.add_trace(
            go.Scatter(
                y=df['Fechamento'], x=df['Data'], mode='lines', name='Fechamento'
            )
        )

        for model in model_selected:
            df_aux = df[df['Modelo'] == model]
            fig.add_trace(
                go.Scatter(
                    y=df_aux['Previsão'], x=df_aux['Data'], mode='lines', name=model
                )
            )


    fig.update_layout(
        title='Preço do Petróleo Brent (2024)',
        xaxis_title='Data',
        yaxis_title='Preço de Fechamento (USD)',
        xaxis=dict(
            rangeslider=dict(visible=True),
            type="date"
        )
    )

    st.plotly_chart(fig)


def get_next_prediction():
    next_pred = pd.DataFrame(db.get_last_prediction(), columns=['id', 'value', 'model'])
    next_pred_meta = next_pred[next_pred['model'] == 'meta']['value'].values[0]
    last_close = db.get_last_days(days=1)[0]


    delta = ((next_pred_meta - last_close[2])/last_close[2])*100

    col1, col2, col3 = st.columns([5,1,2])
    col1.markdown("Veja a próxima previsão do preço do Petróleo Brent de acordo com o :blue-background[Meta-Modelo]")
    col3.metric(":blue[Previsão Meta-Modelo]", f"U$D {next_pred_meta:.2f}", f"{delta:.2f}%", "normal" if delta >= 0 else "negative")

    with col1.expander("Previsão dos outros modelos"):
        st.markdown(f":gray-background[Média] U$D {next_pred['value'].mean():.2f}")
        st.markdown(f":gray-background[KNN] U$D {next_pred[next_pred['model'] == 'knn']['value'].values[0]:.2f}")
        st.markdown(f":gray-background[SVM] U$D {next_pred[next_pred['model'] == 'svm']['value'].values[0]:.2f}")
        st.markdown(f":gray-background[XGBoost] U$D {next_pred[next_pred['model'] == 'xgb']['value'].values[0]:.2f}")
        st.markdown(f":gray-background[Bayesian Ridge] U$D {next_pred[next_pred['model'] == 'br']['value'].values[0]:.2f}")
        st.markdown(f":gray-background[Multi Layer Perceptron] U$D {next_pred[next_pred['model'] == 'mlp']['value'].values[0]:.2f}")


def get_table_predictions():
    df = get_predictions()
    mae_media = df['Diferença'].abs().mean()
    mae_meta = df[df['Modelo'] == 'Meta-Modelo']['Diferença'].abs().mean()
    mae_knn = df[df['Modelo'] == 'KNN']['Diferença'].abs().mean()
    mae_svm = df[df['Modelo'] == 'SVM']['Diferença'].abs().mean()
    mae_xgb = df[df['Modelo'] == 'XGBoost']['Diferença'].abs().mean()
    mae_br = df[df['Modelo'] == 'Bayesian Ridge']['Diferença'].abs().mean()
    mae_mlp = df[df['Modelo'] == 'Multi Layer Perceptron']['Diferença'].abs().mean()

    col1, col2, col3 = st.columns([5,1,2])
    col1.markdown("Média dos erros absolutos das últimas previsões dos modelos para o valor de fechaento do Petróleo Brent")
    col3.metric(":blue-background[MAE Meta-Modelo]", f"U$D {mae_meta:.2f}")

    st.markdown("<div style='margin-bottom: 20px'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    col1.metric(":gray-background[MAE Média]", f"±U$D {mae_media:.2f}")
    col2.metric(":gray-background[MAE KNN]", f"±U$D {mae_knn:.2f}")
    col3.metric(":gray-background[MAE SVM]", f"±U$D {mae_svm:.2f}")
    
    col1.metric(":gray-background[MAE XGBoost]", f"±U$D {mae_xgb:.2f}")
    col2.metric(":gray-background[MAE Bayesian Ridge]", f"±U$D {mae_br:.2f}")
    col3.metric(":gray-background[MAE Multi Layer Perceptron]", f"±U$D {mae_mlp:.2f}")

    st.divider()
    st.markdown("### Tabela de Previsões")
    st.markdown("Veja abaixo as últimas previsões dos modelos para o preço de fechamento do Petróleo Brent")

    st.dataframe(df, width=1000, height=600)
