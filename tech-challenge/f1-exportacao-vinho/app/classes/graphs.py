import streamlit as st
import plotly.express as px
import polars as pl
from . import functions as f


# Plotar Globo com a quantidade de litros exportados por país
def graph_globe(df: pl.DataFrame) -> px:
    df_aux = (
        df.filter(pl.col("liters") > 1000)
        .group_by(["continent", "iso_code", "country"])
        .agg(pl.sum("value"))
    )

    fig = px.scatter_geo(
        df_aux,
        locations="iso_code",
        size="value",
        color="continent",
        projection="orthographic",
        size_max=50,
        custom_data=["value", "country", "continent"],
    )

    fig.update_traces(
        hovertemplate="<b>%{customdata[1]}</b><br>%{customdata[0]} Litros<extra>%{customdata[2]}</extra>"
    )

    fig.update_layout(
        title={
            "text": "Total de Litros de vinho Vendidos por País",
            "xanchor": "center",
            "xref": "paper",
            "yanchor": "top",
            "x": 0.5,
            "y": 0.95,
            "font": {"size": 20},
        },
        template="seaborn",
        height=500,
        margin={"l": 10, "r": 10, "b": 80, "t": 70, "pad": 5},
        legend={
            "orientation": "v",
            "yanchor": "middle",
            "xanchor": "center",
            "x": 1,
            "y": 0.5,
            "title": "",
            "itemsizing": "constant",
        },
    )

    return fig


def table_info(df: pl.DataFrame) -> pl.DataFrame:
    return df.select(
        pl.lit("Brasil").alias("País de Origem"),
        pl.col("country").alias("País de Destino"),
        pl.col("year").alias("Ano de Referência"),
        pl.col("liters").alias("Quantidade de Vinho Exportado (Litros)"),
        pl.col("value").alias("Valor Total Exportado (US$)"),
    )


def graph_one(df: pl.DataFrame, config:dict) -> None:
   
    if not config['decade']:
        df_aux = df.group_by("year").agg(pl.sum("value"))
        group = "year"
        hovertemplate = "<b>Ano de %{x}</b><br>U$ %{value:.2f}"
    else:
        df_aux = (
            df.select((pl.col("year") // 10 * 10).alias("decade"), pl.col("*"))
            .group_by("decade")
            .agg(pl.sum("value"))
        )
        group = "decade"
        hovertemplate = "<b>Década de %{x}</b><br>U$ %{value:.2f}"

    fig = px.bar(df_aux, x=group, y="value")

    f.layout_graphs(
        fig,
        title_text="Valor Total Exportado (US$)",
        title_sup="Gráfico de Barras exibindo o valor total de vinhos exportados ao longo dos anos",
        xaxis={"title": "Ano de Referência"},
        yaxis={"title": "Valor Total Exportado (US$)"},
        hovertemplate=hovertemplate,
        marker_color="#794A9E"
    )

    return fig

def graph_two(df: pl.DataFrame, config: dict) -> None:

    var = "value" if config['metric'] == "Valor Exportado" else "liters"
    func = pl.sum if config['agg'] == "Valor Total" else pl.mean

    df_aux = df.group_by("continent").agg(func(var)).sort(var, descending=True)
    fig = px.bar(df_aux, x="continent", y=var)

    layout_info = {
        "Valor Exportado": {
            "Valor Total": {
                "yaxis": {"title": "Valor Total Exportado (US$)"},
                "hovertemplate": "<b>%{x}</b><br>Total: U$ %{y}",
                "title": "Valor Total Exportado por Região",
                "sup": "Gráfico de Barras exibindo o valor total de vinhos exportado (em US$) para cada região do mundo",
            },
            "Valor Médio": {
                "yaxis": {"title": "Valor Médio Exportado (US$)"},
                "hovertemplate": "<b>%{x}</b><br>Média: U$ %{y}",
                "title": "Valor Médio Exportado por Região",
                "sup": "Gráfico de Barras exibindo o valor médio de vinho exportado (em US$) para cada região do mundo",
            },
        },
        "Litros Exportados": {
            "Valor Total": {
                "yaxis": {"title": "Total de Vinho Exportados (Litros)"},
                "hovertemplate": "<b>%{x}</b><br>Total: %{y} Litros",
                "title": "Volume de Vinho Exportado por Região",
                "sup": "Gráfico de Barras exibindo o volume total de vinho exportado (em litros) para cada região do mundo",
            },
            "Valor Médio": {
                "yaxis": {"title": "Volume Médio de Vinho Exportado (Litros)"},
                "hovertemplate": "<b>%{x}</b><br>Média: %{y} Litros",
                "title": "Volume Médio de Vinho Exportado por Região",
                "sup": "Gráfico de Barras exibindo o volume médio de vinho exportado (em litros) para cada região do mundo",
            },
        },
    }
    
    layout_info_selected = layout_info[config['metric']][config['agg']]

    f.layout_graphs(
        fig,
        yaxis=layout_info_selected["yaxis"],
        xaxis={"title": "Região"},
        hovertemplate=layout_info_selected["hovertemplate"],
        title_text=layout_info_selected["title"],
        title_sup=layout_info_selected["sup"],
        marker_color="#794A9E"
    )
    
    return fig

# Gráfico 3 - Mapa - Valores Totais/Média por País
def graph_three(df: pl.DataFrame, config: dict) -> None:

    var = "value" if config['metric'] == "Valor Exportado" else "liters"
    func = pl.sum if config['agg'] == "Valor Total" else pl.mean
    year = config['year']

    df_aux = (
        df.filter((pl.col("year") >= year[0]) & (pl.col("year") <= year[1]))
        .group_by(["continent", "iso_code", "country"])
        .agg(func(var))
        .sort("continent")
    )

    fig = px.scatter_geo(
        df_aux,
        locations="iso_code",
        size=var,
        color="continent",
        projection="natural earth",
        size_max=30,
        custom_data=["country", var],
        color_discrete_map={
            "Oceania": "#636EFA",
            "América Central e Caribe": "#EF553B",
            "América do Norte": "#00CC96",
            "África": "#AB63FA",
            "Europa": "#FFA15A",
            "Oriente Médio": "#19D3F3",
            "América do Sul": "#FECB52",
            "Ásia": "#FF6692",
        },
    )

    layout_info = {
        "Valor Exportado": {
            "Valor Total": {
                "yaxis": {"title": "Valor Total Exportado (US$)"},
                "hovertemplate": "<b>%{customdata[0]}</b><br>Total: U$ %{customdata[1]}",
                "title": "Valor Total Exportado (US$) por País",
                "sup": "Mapa exibindo o valor total de vinho exportado (em US$) para cada país do mundo",
            },
            "Valor Médio": {
                "yaxis": {"title": "Valor Médio Exportado (US$)"},
                "hovertemplate": "<b>%{customdata[0]}</b><br>Média: U$ %{customdata[1]:.2f}",
                "title": "Valor Médio Exportado por País",
                "sup": "Mapa exibindo o valor médio de vinho exportado (em US$) para cada país do mundo",
            },
        },
        "Litros Exportados": {
            "Valor Total": {
                "yaxis": {"title": "Total de Vinho Exportados (Litros)"},
                "hovertemplate": "<b>%{customdata[0]}</b><br>Total: %{customdata[1]} Litros",
                "title": "Total de Vinho Exportados por País",
                "sup": "Mapa exibindo o volume total de vinho exportado (em litros) para cada país do mundo",
            },
            "Valor Médio": {
                "yaxis": {"title": "Volume Médio de Vinho Exportado (Litros)"},
                "hovertemplate": "<b>%{customdata[0]}</b><br>Média: %{customdata[1]:.2f} Litros",
                "title": "Volume Médio de Vinho Exportado por País",
                "sup": "Mapa exibindo o volume médio de vinho exportado (em litros) para cada país do mundo",
            },
        },
    }
    
    layout_info_selected = layout_info[config['metric']][config['agg']]

    f.layout_graphs(
        fig,
        yaxis=layout_info_selected["yaxis"],
        xaxis={"title": "Continente"},
        hovertemplate=layout_info_selected["hovertemplate"],
        legend={
            "orientation": "h",
            "yanchor": "middle",
            "xanchor": "center",
            "x": 0.5,
            "y": -0.1,
            "title": "",
            "itemsizing": "constant",
        },
        title_text=layout_info_selected["title"],
        title_sup=layout_info_selected["sup"]
    )

    return fig

# Gráfico 4- Mapa - Valores Exportado por País por Ano
def graph_four(df: pl.DataFrame, config:dict) -> None:
    cols = st.columns([2, 1], gap="large")
    col_name = config['col_name']
    
    if config['viz'] == "Customizar":
        list_selected = config['list_selected']
    else:
        df_list_country = (
            df.select(pl.col(col_name, "country"))
            .group_by("country")
            .agg(pl.sum(col_name))
            .sort(col_name, descending=True)
            .limit(3)
        )

        list_selected = df_list_country.select(pl.col("country")).to_series().to_list()  

    with cols[0]:

        df_aux = (
            df.select(pl.col(col_name, "country", "year"))
            .with_columns(
                pl.when(pl.col("country").is_in(list_selected))
                .then(pl.col("country"))
                .otherwise(pl.lit("Outros"))
                .alias("group"),
                pl.when(pl.col("country").is_in(list_selected))
                .then(pl.col(col_name))
                .otherwise(0)
                .alias("order"),
            )
            .group_by("year", "group")
            .agg(pl.sum(col_name), pl.sum("order"))
            .sort(["year", "order"])
        )

        fig = px.line(
            df_aux,
            x="year",
            y=col_name,
            color="group",
            color_discrete_sequence=px.colors.qualitative.Plotly,
            color_discrete_map={"Outros": "#ccc"},
            markers=True,
        )

        layout_info = {
            "Valor Exportado": {
                "yaxis": {"title": "Valor Total Exportado (US$)"},
                "hovertemplate": "<b>%{x}</b><br>U$ %{y}",
                "title": "Valor Total Exportado nos Anos de Referência",
                "sup": "Gráfico de Linha exibindo o valor total de vinho exportado (em US$) por país ao longo do tempo",
            },
            "Litros Exportados": {
                "yaxis": {"title": "Total de Vinho Exportados (Litros)"},
                "hovertemplate": "<b>%{x}</b><br>%{y} Litros",
                "title": "Total de Vinho Exportados nos Anos de Referência",
                "sup": "Gráfico de Linha exibindo o volume total de vinho exportado (em litros) por país ao longo do tempo",
            },
        }
        
        layout_info_selected = layout_info[config['metric']]

        f.layout_graphs(
            fig,
            yaxis=layout_info_selected["yaxis"],
            xaxis={"title": "Ano de Referência"},
            hovertemplate=layout_info_selected["hovertemplate"],
            legend={
                "orientation": "h",
                "yanchor": "middle",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.3,
                "title": "",
                "itemsizing": "constant",
                "traceorder": "reversed",
            },
            title_text=layout_info_selected["title"],
            title_sup=layout_info_selected["sup"]
        )
        
    return fig

# Gráfico 5 - Preço Médio por Ano
def graph_five(df: pl.DataFrame, config:dict) -> None:

    if not config['median_region']:
        df_aux = (
            df.filter(pl.col("price_per_liter") > 0)
            .group_by(["year"])
            .agg(pl.median("price_per_liter"))
            .sort("year")
        )
        fig = px.line(df_aux, x="year", y="price_per_liter")
        hovertemplate = "<b>Ano de %{x}</b><br>U$ %{y:.2f}"
        titlex = "Ano de Referência"
        title = "Preço mediano por litro por Ano"
        title_sup = "Gráfico de Linha exibindo o preço mediano por litro de vinho exportado (em US$) ao longo do tempo"
        line_color = "#794A9E"
        marker_color = ""
    else:
        df_aux = (
            df.filter(pl.col("price_per_liter") > 0)
            .group_by(["continent"])
            .agg(pl.median("price_per_liter"))
            .sort("price_per_liter", descending=True)
        )
        fig = px.bar(df_aux, x="continent", y="price_per_liter")
        hovertemplate = "<b>%{x}</b><br>U$ %{y:.2f}"
        titlex = "Região"
        title = "Preço mediano por litro (US$) por Região"
        title_sup = "Gráfico de Linha exibindo o preço total mediano por litro de vinho exportado (em US$) para cada região do mundo"
        line_color = ""
        marker_color = "#794A9E"

    f.layout_graphs(
        fig,
        xaxis={"title": titlex},
        yaxis={"title": "Preço mediano por Litro (US$)"},
        hovertemplate=hovertemplate,
        legend={
            "orientation": "h",
            "yanchor": "middle",
            "xanchor": "center",
            "x": 0.5,
            "y": -0.3,
            "title": "",
            "itemsizing": "constant",
            "traceorder": "reversed",
        },
        title_text=title,
        title_sup=title_sup,
        line_color=line_color,
        marker_color=marker_color
        
    )


    return fig