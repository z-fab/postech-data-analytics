import base64
import streamlit as st
import polars as pl
import plotly.express as px

import graphs as g


@st.cache_data
def load_data() -> pl.DataFrame:
    return pl.read_csv("data/dataframe_final.csv")


def displayPDF(file):
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")

    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="400px" type="application/pdf"></iframe>'

    st.markdown(pdf_display, unsafe_allow_html=True)


def configurar_streamlit() -> None:
    st.set_page_config(
        page_title="Tech Challenge: Exportação de Vinho",
        page_icon="🍷",
        layout="wide",
    )

    return None


def criar_header() -> None:
    st.markdown("# Tech Challenge: :violet[Exportação de Vinho]")
    st.markdown(
        ":gray[Tech Challenge é o projeto final de fase da **PósTech**, ele engloba os conhecimentos obtidos em todas as disciplinas vistas até aquele momento.]"
    )
    st.markdown(
        """
        **Contexto:**
        Somos o Expert em Data Analytics em uma empresa que exporta vinhos do Brasil para o mundo todo. Sua área é recém-criada dentro da empresa, e você será responsável pelos relatórios iniciais a serem apresentados em uma reunião de investidores e acionistas, explicando a quantidade de vinhos exportados e os fatores externos que podem vir a surgir e que interferem nas análises
        
        **Fonte de Dados:** [Banco de dados de uva, vinho e derivados](http://vitibrasil.cnpuv.embrapa.br/)
        """
    )

    return None


def tab_intro(df: pl.DataFrame) -> None:
    cols1, cols2 = st.columns(spec=[2, 2])

    with cols1:
        st.markdown("a")

    with cols2:
        st.plotly_chart(g.graph_globo(df), use_container_width=True)

    st.markdown(
        """
        ###### Tabela com informações sobre a exportação de vinho
        Tabela contendo as informações solicitadas sobre a exportação de vinho, como país de origem, país de destino, ano de referência, quantidade de vinho exportado (em litros) e valor total exportado (em US$)
        """
    )
    st.dataframe(g.table_info(df), use_container_width=True)

    return None


def tab_tabela(df: pl.DataFrame) -> None:
    st.markdown(
        """
        ###### Tabela Geral
        Tabela contendo todas as informações sobre a exportação de vinho e os paises de destino
        """
    )

    with st.expander("📄 Descrição dos Campos", expanded=False):
        st.markdown(
            """
                **Ano de Referência**: Ano em que a exportação foi realizada
                \n**País de Destino**: País para onde o vinho foi exportado
                \n**População do País**: População do País no ano de referência
                \n**Idade Média do** País: Idade Média do País no ano de referência
                \n**Dens. Pop**. do País: Densidade Populacional do País no ano de referência
                \n**Razão de Sexo** do País: Número de Homens para cada 100 Mulheres no ano de referência
                \n**Vinho Exportado (Litros**): Quantidade de Vinho Exportado (em Litros)
                \n**Vinho Exportado por** Pessoa (Litros): Quantidade de Vinho Exportado por Pessoa (em Litros)
                \n**Valor Exportado (US**\$): Valor Total Exportado (em US\$)
                \n**Preço do Vinho** (US\$/Litro): Preço do Vinho em US\$/Litro
            """
        )

    df_aux = (
        df.select(
            pl.col("year").alias("Ano de Referência"),
            pl.col("country").alias("País de Destino"),
            pl.col("population").alias("População do País"),
            pl.col("median_age").alias("Idade Média do País"),
            pl.col("pop_density").alias("Dens. Pop. do País"),
            pl.col("sex_ratio").alias("Razão de Sexo do País"),
            pl.col("liters").alias("Vinho Exportado (Litros)"),
            pl.col("liters_per_capita").alias("Vinho Exportado por Pessoa (Litros)"),
            pl.col("value").alias("Valor Exportado (US$)"),
            pl.col("price_per_liter").alias("Preço do Vinho (US$/Litro)"),
        )
        .fill_nan(0)
        .fill_null(0)
    )

    st.dataframe(
        df_aux,
        use_container_width=True,
        column_config={
            "Valor Exportado (US$)": st.column_config.NumberColumn(
                "Valor Exportado (US$)",
                help="Valor Total Exportado (em US\$)",
                format="US$ %.2f",
            ),
            "Preço do Vinho (US$/Litro)": st.column_config.NumberColumn(
                "Preço do Vinho (US$/Litro)",
                help="Preço do Vinho em US\$/Litro",
                format="US$ %.2f",
            ),
        },
    )

    return None


def tab_graph(df: pl.DataFrame) -> None:
    st.markdown("<div style='margin-bottom: 40px'></div>", unsafe_allow_html=True)
    g.graph_valor_total_ano(df)
    g.graph_valor_total_continente(df)
    g.graph_valor_total_pais_mapa(df)
    g.graph_valor_pais(df, n=1)

    cols = st.columns(2, gap="large")
    with cols[0]:
        g.graph_valor_medio_ano(df)
    with cols[1]:
        g.graph_litro_preco(df)

    return None


if __name__ == "__main__":
    configurar_streamlit()
    df = load_data()
    criar_header()

    tabs = st.tabs(["🌎 Introdução", "📋 Tabela", "📊 Gráficos"])

    with tabs[0]:
        tab_intro(df)

    with tabs[1]:
        tab_tabela(df)

    with tabs[2]:
        tab_graph(df)
