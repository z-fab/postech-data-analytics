import streamlit as st
import polars as pl
import plotly.express as px
from . import graphs as g
from . import functions as f
from . import structure as s

def struct_graph_one(df: pl.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            decade = st.toggle("Agrupar por Década", key="decade_graph_one")
        
        config_graph["decade"] = decade
        struct_description(
            "Podemos ver que o valor total exportado (em US$) apresenta dois momentos, um na década de 90 e outro no ano de 2013.<br><br>\
            O aumento na década de 90 é resultado da abertura comercial ocorrida no Brasil nesse período e aos esforços da Cooperativa Vinícola Aurora, que tentou penetrar no mercado norte-americano nesse período.<br><br>\
            Já o pico em 2013 se deve, em partes, a políticas do governo federal no PEP (Programa de Escoamento da Produção), especialmente quando exportados para a Rússia e, também, ao programa de exportação Wine of Brasil."
        )
            
    with cols[0]:
        
        fig = g.graph_one(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)

    return None

def struct_graph_two(df: pl.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    
    with cols[1]:
        
        
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            metric = st.selectbox(
                "Métrica",
                ("Valor Exportado", "Litros Exportados"),
                key="metric_graph_two",
            )
            agg = st.selectbox(
                "Visualização", ("Valor Total", "Valor Médio"),
                key="agg_graph_two",
            )
        
        config_graph["metric"] = metric
        config_graph["agg"] = agg
        struct_description('Podemos ver que em relação ao valor total exportado (em US$) desde a década de 70, os países da América do Sul se mostraram nosso principal importador de Vinho.<br><br>\
                            Porém ao analisar o mesmo gráfico verificando o valor médio das exportações (quanto cada país pagou por exportação), verificamos que os países da América do Norte pagam mais, ou seja: importaram uma quantidade menor porém por um valor maior.')
            
    with cols[0]:
        
        fig = g.graph_two(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)

    return None

def struct_graph_three(df: pl.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    
    
    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            year = st.slider(
                "Período", 1970, 2022, (1970, 2022),
                key="year_graph_three"
            )
            metric = st.selectbox(
                "Métrica",
                ("Valor Exportado", "Litros Exportados"),
                key="metric_graph_three",
            )
            agg = st.selectbox(
                "Visualização",
                ("Valor Total", "Valor Médio"),
                key="agg_graph_three",
            )
        
        config_graph["metric"] = metric
        config_graph["agg"] = agg
        config_graph["year"] = year
        struct_description('O continente Americano (Sul, Central e Norte) é o principal destino das exportações. O Paraguai é nosso maior importador, seguido dos Estados Unidos e Rússia.<br><br>Esse alto volume de importação paraguaia pode ser explicado pelo fato de o Brasil e o Paraguai serem os únicos países nos quais os vinhos de uvas americanas e híbridas são pre-dominantes <a target="_blank" href="https://web.bndes.gov.br/bib/jspui/bitstream/1408/2603/1/BS%2019%20Desafios%20da%20vitinicultura%20brasileira_P.pdf">[Fonte]</a>.')
            
    with cols[0]:
        
        fig = g.graph_three(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)

    return None

def struct_graph_four(df: pl.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    
    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            metric = st.selectbox(
                "Métrica",
                ("Valor Exportado", "Litros Exportados"),
                key="metric_graph_four",
            )
            viz = st.selectbox("Visualização", ("Top 3 Países", "Customizar"), key="viz_graph_four")
            
            var = {"Valor Exportado": "value", "Litros Exportados": "liters"}
            col_name = var[metric]
            
            if viz == "Customizar":
                list_name = (
                    df.select(pl.col("country"), pl.col(col_name))
                    .group_by("country")
                    .agg(pl.sum(col_name))
                    .sort(col_name, descending=True)
                    .select(pl.col("country"))
                    .to_series()
                    .to_list()
                )
                config_graph['list_selected'] = st.multiselect("Paises selecionados", list_name)
            
        
        config_graph["metric"] = metric
        config_graph["viz"] = viz
        config_graph["col_name"] = col_name
        struct_description('Apesar de o Brasil exportar a maioria do vinho para o Paraguai e ele apresentar mais constância, os Estados Unidos e Rússia se mostram potenciais mercados importadores, em muitos anos ultrapassando em muito, o Paraguai em valor total exportado.')
            
    with cols[0]:
        
        fig = g.graph_four(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.markdown("<div style='margin-bottom: 30px'></div>", unsafe_allow_html=True)

    return None

def struct_graph_five(df: pl.DataFrame) -> None:
    
    config_graph = {}
    cols = st.columns([2, 1], gap="large")
    
    
    with cols[1]:
        with st.expander("⚙️ Configuração do Gráfico", expanded=False):
            median_region = st.toggle("Ver Preço mediano total por Região", key="median_region_graph_five")
        
        config_graph["median_region"] = median_region
        struct_description('Ao analisarmos o preço mediano do litro do vinho exportado podemos perceber que há uma tendência de alta no valor a partir de 2009.<br><br>\
                            Além disso, quando olhamos por região, apesar da Oceania ser uma das regiões para a qual menos exportamos vinho, o litro do vinho exportado para lá é o mais elevado, seguido pelo Oriente Médio.')
            
    with cols[0]:
        
        fig = g.graph_five(df, config_graph)
        st.plotly_chart(fig, use_container_width=True)

    return None

def struct_description(text: str) -> None:
    st.markdown(
        f"""
        <div style="background: #f8f8f8; padding: 20px 25px 10px 20px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 100px">
            <p style="text-align: left; font-size:13px; color: #bbb">
                💡 Análise
            </p>
            <p style="text-align: left;">
                {text}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return None

def header() -> None:
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
    
    with st.expander("↓ Download dos Arquivos", expanded=False):
        
        with open('./content/apresentacao.pdf', "rb") as file:
            btn = st.download_button(
                label="📽️ Baixar Apresentação",
                data=file,
                file_name="winetech_apresentacao.pdf",
                mime="application/pdf",
                type='primary',
                key="download_apresentacao"
            )
             
        with open('./content/tabela.xlsx', 'rb') as file:
            btn = st.download_button(
                label="📊 Baixar Excel",
                data=file,
                file_name="tabela_exportacao.xlsx",
                mime='application/vnd.ms-excel',
                type='primary',
                key="download_excel"
            )
            
        with open('./data/dataframe_final.csv', 'rb') as file:
            btn = st.download_button(
                label="💿 Baixar CSV completo",
                data=file,
                file_name="data.csv",
                mime='text/csv',
                type='primary',
                key="download_csv"
            )
            
    st.markdown("<div style='margin-bottom: 40px'></div>", unsafe_allow_html=True)


    return None

def tab_intro(df: pl.DataFrame) -> None:
    
    cols1, cols2 = st.columns(spec=[2, 2])
    with cols1:
        f.displayPDF("./content/apresentacao.pdf")

    with cols2:
        st.plotly_chart(g.graph_globe(df), use_container_width=True)

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
    
    s.struct_graph_one(df)
    s.struct_graph_two(df)
    s.struct_graph_three(df)
    s.struct_graph_four(df)
    s.struct_graph_five(df)

    return None