import streamlit as st
import plotly.graph_objects as go
import polars as pl


def graph_faltas(df):
    df_aux = (
        df.with_columns(
            pl.col("data_aula").dt.strftime("%Y/%m").alias("data"),
        )
        .group_by(["data"])
        .agg(
            pl.col("presente").is_in([0]).sum().alias("faltou"),
            pl.col("presente").is_in([1]).sum().alias("compareceu"),
        )
        .sort("data")
    )

    media_faltas = df_aux["faltou"].mean()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_aux["data"],
            y=df_aux["faltou"],
            mode="lines+markers",
            name="Faltas",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_aux["data"],
            y=[media_faltas] * len(df_aux),
            mode="lines",
            name="Média de Faltas",
            line=dict(color="gray", width=2, dash="dash"),
        )
    )

    # Personalizando o layout
    fig.update_layout(
        title="Quantidade de Faltas ao Longo do Tempo",
        xaxis_title="Data",
        yaxis_title="Número de Faltas",
        template="plotly_white",
    )

    # Exibindo o gráfico
    st.plotly_chart(fig)


def graph_faltas_aluno(df_aluno):
    df_aux = (
        df_aluno.with_columns(
            pl.col("data_aula").dt.strftime("%Y/%m").alias("data"),
        )
        .group_by(["data"])
        .agg(
            pl.col("presente").is_in([0]).sum().alias("faltou"),
            pl.col("presente").is_in([1]).sum().alias("compareceu"),
        )
        .sort("data")
    )

    media_faltas = df_aux["faltou"].mean()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df_aux["data"],
            y=df_aux["faltou"],
            mode="lines+markers",
            name="Faltas",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df_aux["data"],
            y=[media_faltas] * len(df_aux),
            mode="lines",
            name="Média de Faltas",
            line=dict(color="gray", width=2, dash="dash"),
        )
    )

    # Personalizando o layout
    fig.update_layout(
        title="Quantidade de Faltas ao Longo do Tempo",
        xaxis_title="Data",
        yaxis_title="Número de Faltas",
        template="plotly_white",
    )

    # Exibindo o gráfico
    st.plotly_chart(fig)
