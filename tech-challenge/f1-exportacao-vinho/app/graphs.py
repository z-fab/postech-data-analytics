import streamlit as st
import plotly.express as px
import polars as pl
import functions as f


# Plotar Globo com a quantidade de litros exportados por país
def graph_globo(df: pl.DataFrame) -> px:
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


# Gráfico 4- Mapa - Valores Exportado por País por Ano
def graph_valor_pais(df: pl.DataFrame, var="value", n=5) -> None:
    cols = st.columns([2, 1], gap="large")
    var = {"Valor Exportado": "value", "Litros Exportados": "liters"}
    custom_str = {"Valor Exportado": "Valor: ", "Litros Exportados": "Litros: "}

    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=True):
            metrica = st.selectbox(
                "Qual métrica deseja visualizar?",
                ("Valor Exportado", "Litros Exportados"),
                key="metrica_temporal",
            )
            type = st.selectbox(
                "Visualização deseja ver?", ("Top 3 Países", "Customizar")
            )

            if type == "Customizar":
                list_name = (
                    df.select(pl.col("country"), pl.col(var[metrica]))
                    .group_by("country")
                    .agg(pl.sum(var[metrica]))
                    .sort(var[metrica], descending=True)
                    .select(pl.col("country"))
                    .to_series()
                    .to_list()
                )
                list_selected = st.multiselect("Paises a serem visualizados", list_name)

    with cols[0]:
        df_aux = (
            df.select(pl.col(var[metrica], "country"))
            .group_by("country")
            .agg(pl.sum(var[metrica]))
            .sort(var[metrica], descending=True)
            .limit(3)
        )
        if type != "Customizar":
            list_selected = df_aux.select(pl.col("country")).to_series().to_list()

        df_aux2 = (
            df.select(pl.col(var[metrica], "country", "year"))
            .with_columns(
                pl.when(pl.col("country").is_in(list_selected))
                .then(pl.col("country"))
                .otherwise(pl.lit("Outros"))
                .alias("group"),
                pl.when(pl.col("country").is_in(list_selected))
                .then(pl.col(var[metrica]))
                .otherwise(0)
                .alias("order"),
            )
            .group_by("year", "group")
            .agg(pl.sum(var[metrica]), pl.sum("order"))
            .sort(["year", "order"])
        )

        fig = px.line(
            df_aux2,
            x="year",
            y=var[metrica],
            color="group",
            color_discrete_sequence=px.colors.qualitative.Plotly,
            color_discrete_map={"Outros": "#ccc"},
            markers=True,
        )

        layout = {
            "Valor Exportado": {
                "yaxis": {"title": "Valor Total Exportado (US$)"},
                "hovertemplate": "<b>%{x}</b><br>U$ %{y}",
                "title": "Valor Total Exportado (US$) nos Anos de Referência",
            },
            "Litros Exportados": {
                "yaxis": {"title": "Total de Vinho Exportados (Litros)"},
                "hovertemplate": "<b>%{x}</b><br>%{y} Litros",
                "title": "Total de Vinho Exportados (Litros) nos Anos de Referência",
            },
        }

        f.layout_graphs(
            fig,
            yaxis=layout[metrica]["yaxis"],
            xaxis={"title": "Ano de Referência"},
            hovertemplate=layout[metrica]["hovertemplate"],
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
        )

        st.plotly_chart(fig, use_container_width=True)

    f.descricao(
        title=layout[metrica]["title"],
        text="Apesar de o Brasil exportar a maioria do vinho para o Paraguai, os Estados Unidos se mostra um mercado lucrativo, em muitos anos ultra passando o Paraguai em valor total exportado.",
    )


# Gráfico 3 - Mapa - Valores Totais/Média por País
def graph_valor_total_pais_mapa(df: pl.DataFrame) -> None:
    cols = st.columns([2, 1], gap="large")

    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=True):
            year = st.slider(
                "Qual período gostaria de visualizar?", 1970, 2022, (1970, 2022)
            )
            metrica = st.selectbox(
                "Qual métrica deseja visualizar?",
                ("Valor Exportado", "Litros Exportados"),
                key="metrica_mapa",
            )
            agg = st.selectbox(
                "Qual agregação deseja fazer?",
                ("Valor Total", "Valor Médio"),
                key="agg_mapa",
            )

    with cols[0]:
        var = "value" if metrica == "Valor Exportado" else "liters"
        func = pl.sum if agg == "Valor Total" else pl.mean

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

        layout = {
            "Valor Exportado": {
                "Valor Total": {
                    "yaxis": {"title": "Valor Total Exportado (US$)"},
                    "hovertemplate": "<b>%{customdata[0]}</b><br>Total: U$ %{customdata[1]}",
                    "title": "Valor Total Exportado (US$) por País",
                },
                "Valor Médio": {
                    "yaxis": {"title": "Valor Médio Exportado (US$)"},
                    "hovertemplate": "<b>%{customdata[0]}</b><br>Média: U$ %{customdata[1]:.2f}",
                    "title": "Valor Médio Exportado (US$) por País",
                },
            },
            "Litros Exportados": {
                "Valor Total": {
                    "yaxis": {"title": "Total de Vinho Exportados (Litros)"},
                    "hovertemplate": "<b>%{customdata[0]}</b><br>Total: %{customdata[1]} Litros",
                    "title": "Total de Vinho Exportados (Litros) por País",
                },
                "Valor Médio": {
                    "yaxis": {"title": "Volume Médio de Vinho Exportado (Litros)"},
                    "hovertemplate": "<b>%{customdata[0]}</b><br>Média: %{customdata[1]:.2f} Litros",
                    "title": "Volume Médio de Vinho Exportado (Litros) por País",
                },
            },
        }

        f.layout_graphs(
            fig,
            yaxis=layout[metrica][agg]["yaxis"],
            xaxis={"title": "Continente"},
            hovertemplate=layout[metrica][agg]["hovertemplate"],
            legend={
                "orientation": "h",
                "yanchor": "middle",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.1,
                "title": "",
                "itemsizing": "constant",
            },
        )

        st.plotly_chart(fig, use_container_width=True)

    f.descricao(
        title=layout[metrica][agg]["title"],
        text="Podemos ver que a América do Sul é o continente cujo o qual a maioria da exportação acontece. Em seguida vem a América do Norte e Europa. Esse comportamento permanece o mesmo caso olhemos para a exportação de Vinho ou para o valor Médio",
    )

    return None


# Gráfico 2 - Grafico de barra - Valores Totais/Média por Região
def graph_valor_total_continente(df: pl.DataFrame) -> None:
    cols = st.columns([2, 1], gap="large")

    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=True):
            metrica = st.selectbox(
                "Qual métrica deseja visualizar?",
                ("Valor Exportado", "Litros Exportados"),
            )
            agg = st.selectbox(
                "Qual agregação deseja fazer?", ("Valor Total", "Valor Médio")
            )

    with cols[0]:
        var = "value" if metrica == "Valor Exportado" else "liters"
        func = pl.sum if agg == "Valor Total" else pl.mean

        df_aux = df.group_by("continent").agg(func(var)).sort(var, descending=True)
        fig = px.bar(df_aux, x="continent", y=var)

        layout = {
            "Valor Exportado": {
                "Valor Total": {
                    "yaxis": {"title": "Valor Total Exportado (US$)"},
                    "hovertemplate": "<b>%{x}</b><br>Total: U$ %{y}",
                    "title": "Valor Total Exportado (US$) por Região",
                },
                "Valor Médio": {
                    "yaxis": {"title": "Valor Médio Exportado (US$)"},
                    "hovertemplate": "<b>%{x}</b><br>Média: U$ %{y}",
                    "title": "Valor Médio Exportado (US$) por Região",
                },
            },
            "Litros Exportados": {
                "Valor Total": {
                    "yaxis": {"title": "Total de Vinho Exportados (Litros)"},
                    "hovertemplate": "<b>%{x}</b><br>Total: %{y} Litros",
                    "title": "Total de Vinho Exportados (Litros) por Região",
                },
                "Valor Médio": {
                    "yaxis": {"title": "Volume Médio de Vinho Exportado (Litros)"},
                    "hovertemplate": "<b>%{x}</b><br>Média: %{y} Litros",
                    "title": "Volume Médio de Vinho Exportado (Litros) por Região",
                },
            },
        }

        f.layout_graphs(
            fig,
            yaxis=layout[metrica][agg]["yaxis"],
            xaxis={"title": "Continente"},
            hovertemplate=layout[metrica][agg]["hovertemplate"],
        )

        st.plotly_chart(fig, use_container_width=True)

    f.descricao(
        title=layout[metrica][agg]["title"],
        text="A maior parte das exportações se concentram nas Américas e Europa. O País para quem mais exportamos vinho é o Paraguái seguido pelos Estados Unidos",
    )

    return None


# Gráfico 1 - Valor Total Exportado (US$) por Ano
def graph_valor_total_ano(df: pl.DataFrame) -> None:
    cols = st.columns([2, 1], gap="large")

    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=True):
            type = st.toggle("Agrupar por Década")

    with cols[0]:
        if not type:
            df_aux = df.group_by("year").agg(pl.sum("value"))
            group = "year"
            hovertemplate = "<b>Ano de %{x}</b><br>U$ %{value:.2f}"
        else:
            df_aux = (
                df.select((pl.col("year") // 10 * 10).alias("cut"), pl.col("*"))
                .group_by("cut")
                .agg(pl.sum("value"))
            )
            group = "cut"
            hovertemplate = "<b>Década de %{x}</b><br>U$ %{value:.2f}"

        fig = px.bar(df_aux, x=group, y="value")

        f.layout_graphs(
            fig,
            xaxis={"title": "Ano de Referência"},
            yaxis={"title": "Valor Total Exportado (US$)"},
            hovertemplate=hovertemplate,
        )

        st.plotly_chart(fig, use_container_width=True)

    f.descricao(
        title="Valor Total Exportado (US$) por Ano",
        text="Podemos ver que o valor total exportado (em US$) apresenta dois picos, um na década de 90 e outro em 2013",
    )

    return None


def graph_litro_preco(df: pl.DataFrame) -> None:
    df_aux = df.group_by("country").agg(pl.sum("liters"), pl.mean("price_per_liter"))

    fig = px.scatter(df_aux, y="liters", x="price_per_liter")

    fig.update_layout(
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
        xaxis={
            "title": "Preço Médio do Vinho (por Litro)",
            "tickformat": "$.2f",
        },
        yaxis={
            "title": "Total de vinho vendido (em Litros)",
            "type": "log",
        },
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        """
            <p style="text-align: center; font-size: 20px; color:#7F379A"><b>
                Preço do Vinho (US$/Litro) x Quantidade de Vinho Exportado (Litros)
            </b></p>
            <p style="text-align: center;">
                Podemos ver que existe uma (pequena) correlação positiva entre o preço do vinho e a quantidade de vinho exportado, ou seja, quanto maior o preço do vinho, maior a quantidade de vinho exportado.
            </p>
            """,
        unsafe_allow_html=True,
    )

    return None


def graph_valor_medio_ano(df: pl.DataFrame) -> None:
    df_aux = (
        df.filter(pl.col("liters") > 1000)
        .group_by(["continent", "year"])
        .agg(pl.mean("price_per_liter"))
    )

    fig = px.scatter(df_aux, y="price_per_liter", x="year", color="continent")
    fig = px.scatter(
        df_aux,
        x="year",
        y="price_per_liter",
        color="continent",
        # color_discrete_sequence=px.colors.qualitative.Plotly,
    )

    fig.update_layout(
        template="seaborn",
        height=500,
        margin={"l": 10, "r": 10, "b": 80, "t": 70, "pad": 5},
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
        xaxis={"title": "Ano de Referência"},
        yaxis={"title": "Valor Total Exportado (US$)"},
    )

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        """
            <p style="text-align: center; font-size: 20px; color:#7F379A"><b>
                Valor Total Exportado (US$) por Ano
            </b></p>
            <p style="text-align: center;">
                Podemos ver que o valor total exportado (em US$) apresenta dois picos, um na década de 90 e outro em 2013
            </p>
            """,
        unsafe_allow_html=True,
    )
