import streamlit as st
import polars as pl
from . import controller as ctrl
from backend.predict import predict
from backend.data_process import prepare_data_to_predict


def info(data):
    st.markdown(" ")
    ctrl.graph_faltas(data)
    st.markdown(
        """ 
    <p>Este projeto tem como objetivo desenvolver um modelo de aprendizado de máquina para prever a presença de alunos em aulas futuras.</p>
    <p>O modelo se baseia no histórico do diário de classe e em outras informações relevantes sobre as aulas e os estudantes. Para criar uma visão abrangente e robusta, utilizamos dados provenientes de seis bases distintas, que incluem informações sobre cadastro de alunos, professores, turmas e disciplinas.</p>
    <h3>Desenvolvimento</h3>
    <p>O processo de desenvolvimento começou com a coleta e integração dos dados brutos dessas seis tabelas diferentes. Realizamos um trabalho minucioso de agregação para criar um único conjunto de dados coeso e informativo. Este conjunto de dados consolidado foi então utilizado para treinar nosso modelo de aprendizado de máquina.</p>
    <p>A estrutura da nossa base de dados é fundamental para o funcionamento do modelo. Cada linha representa um aluno específico e contém informações sobre seu comportamento e características durante as dez aulas anteriores. Essa abordagem nos permite capturar padrões temporais na frequência dos alunos e correlacioná-los com outros fatores relevantes.</p>
    <p>Para a modelagem, optamos por utilizar um algoritmo de floresta aleatória, conhecido por sua eficácia em tarefas de classificação e regressão. Este algoritmo nos permite lidar com a complexidade das relações entre as diversas variáveis que influenciam a presença dos alunos.</p>
    <h3>Resultados</h3>
    <p>Como evolução é interessante buscar maneiras de refinar e melhorar o modelo. Isso inclui a exploração de novas features, a experimentação com outros algoritmos e a incorporação de dados adicionais que possam aumentar a precisão de nossas previsões.</p>
    <p>O objetivo final é fornecer uma ferramenta valiosa para a organização e professores, permitindo intervenções proativas para melhorar a assiduidade e, consequentemente, o desempenho acadêmico dos estudantes.</p>
    """,
        unsafe_allow_html=True,
    )


def prev(df_aluno, data):
    lista_aluno = list(df_aluno.sort("nome_id_aluno")["nome_id_aluno"])

    with st.form("my_form"):
        aluno = st.selectbox("Selecione o Aluno", lista_aluno)

        if st.form_submit_button("Prever"):
            df_aluno = df_aluno.filter(pl.col("nome_id_aluno") == aluno)
            id_aluno = df_aluno.select("id_aluno").item(0, 0)

            c1, c2 = st.columns([2, 1])

            resp = prepare_data_to_predict(data, id_aluno)
            proba = predict(resp)

            with c1:
                st.markdown("##### Aluno Selecionado")
                st.markdown(
                    f"""
                    <p style=''>ID: {df_aluno['id_aluno'].item(0)}</p>
                    <p style='margin-top: -15px'>Nome: {df_aluno['nome_aluno'].item(0)}</p>
                    <p style='margin-top: -15px'>Data Nascimento: {df_aluno['data_nascimento_aluno'].item(0)}</p>
                    <p style='margin-top: -15px'>Sexo: {('Masculino' if df_aluno['sexo_aluno'].item(0) == 1 else 'Feminino')}</p>
                    """,
                    unsafe_allow_html=True,
                )

            with c2:
                st.markdown(
                    "<div style='margin-bottom: 40px'></div>", unsafe_allow_html=True
                )
                st.metric(
                    label="Probabilidade de comparecer", value=f"{proba[1]*100:.1f}%"
                )

            ctrl.graph_faltas_aluno(data.filter(pl.col("id_aluno") == id_aluno))


def header():
    st.markdown("# Datathon: :green[Passos Mágicos]")
    st.markdown(
        ":gray-background[Datathon] é o projeto final da **PósTech**, ele engloba os conhecimentos obtidos em todas as disciplinas vistas na pós-graduação."
    )
    st.markdown(
        """
        **Contexto:**
        O grande objetivo do datathon é criar uma proposta preditiva para potencializar o impacto que a ONG “Passos Mágicos” tem realizado sobre a comunidade que atende. 
    """
    )
    st.markdown(
        """
        **Proposta:**
        A proposta é criar um modelo preditivo para, com base em dados históricos, prever a chance de um determinado aluno comparecer à próxima aula da ONG.
    """
    )
    st.markdown(
        """
        <p style="font-size: 14px; color: #AAA; ">
        Projeto criado por <b>Fabricio Zillig</b>. O código fonte está disponível no <a style='color: #999' target='_blank' href='https://github.com/z-fab/postech-data-analytics/tree/master/tech-challenge/f5-passos-magicos'>GitHub</a>
        </p>""",
        unsafe_allow_html=True,
    )
