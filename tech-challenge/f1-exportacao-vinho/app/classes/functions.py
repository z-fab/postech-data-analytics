import streamlit as st
import plotly.express as px
import polars as pl
import base64


@st.cache_data
def load_data() -> pl.DataFrame:
    return pl.read_csv("./data/dataframe_final.csv")


def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" style="margin:60px 0 20px 0" width="95%" height="320px" type="application/pdf"></iframe>'

        st.markdown(pdf_display, unsafe_allow_html=True)


def config_streamlit() -> None:
    st.set_page_config(
        page_title="Tech Challenge: Exportação de Vinho",
        page_icon="🍷",
        layout="wide",
    )

    return None

def layout_graphs(
    fig: px,
    template: str = "seaborn",
    height: int = 500,
    margin: dict = {"l": 10, "r": 10, "b": 10, "t": 85, "pad": 5},
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
    title_text = "-",
    title_sup = "--",
    marker_color = '',
    line_color = '',
    other: dict = dict(),
) -> None:
    dic = dict(
        template=template,
        height=height,
        margin=margin,
        legend=legend,
        xaxis=xaxis,
        yaxis=yaxis,
        title={
            'text': f'{title_text}<br><sup style="color: #888; font-weight: normal;">{title_sup}</sup>',
            'xanchor': 'left',
            'xref': 'paper',
            'yanchor': 'auto',
            'x': 0,
            'y': .95,
            'font': {
                'size': 20,
                'color': '#666'
            }
        },
    )

    fig.update_layout(dic | other)
    
    if marker_color != '':
        fig.update_traces(marker_color = marker_color)
    if line_color != '':
        fig.update_traces(line_color = line_color)
    
    fig.update_traces(hovertemplate=hovertemplate)

    return None
