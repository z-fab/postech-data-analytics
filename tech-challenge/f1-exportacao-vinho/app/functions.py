import streamlit as st
import plotly.express as px
import polars as pl
import plotly.graph_objects as go


def descricao(title: str, text: str) -> None:
    st.markdown(
        f"""
        <div style="background: #f8f8f8; padding: 20px 10px 10px 20px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 100px">
            <p style="text-align: left; font-size: 20px;; color:#7F379A"><b>
                {title}
            </b></p>
            <p style="text-align: left;">
                {text}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return None


def layout_graphs(
    fig: px,
    template: str = "seaborn",
    height: int = 400,
    margin: dict = {"l": 10, "r": 10, "b": 10, "t": 20, "pad": 5},
    legend: dict = {
        "orientation": "v",
        "yanchor": "middle",
        "xanchor": "center",
        "x": 1,
        "y": 0.5,
        "title": "",
        "itemsizing": "constant",
    },
    xaxis: dict = {"title": ""},
    yaxis: dict = {"title": ""},
    hovertemplate: str = "<b>%{x}</b><br>%{y}",
    other: dict = dict(),
) -> None:
    dic = dict(
        template=template,
        height=height,
        margin=margin,
        legend=legend,
        xaxis=xaxis,
        yaxis=yaxis,
    )

    fig.update_layout(dic | other)
    fig.update_traces(hovertemplate=hovertemplate)

    return None
