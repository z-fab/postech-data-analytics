import streamlit as st
from . import controller as ctrl


def dash():
    st.markdown(" ")
    ctrl.get_next_prediction()
    st.divider()
    ctrl.get_prediction_graph()
    st.divider()
    ctrl.get_table_predictions()


def hist():
    ctrl.get_history_graph()
    st.markdown("""
        O preço do petróleo Brent é uma referência global para os preços do petróleo bruto, utilizado como benchmark para precificação. Ele é negociado principalmente em Londres e serve como um indicador importante para o mercado energético mundial. O preço do Brent pode ser influenciado por diversos fatores, incluindo eventos geopolíticos, decisões de produção da OPEP, e crises econômicas.

        A seguir, são relacionados eventos históricos e seus impactos no preço do petróleo Brent, conforme ilustrado no gráfico:

        :red-background[(1) **Setembro de 2008**] - **Crise Financeira Global:**
        A crise financeira de 2008, marcada pela falência do Lehman Brothers, levou a uma queda abrupta nos preços do petróleo devido à diminuição da demanda global. No gráfico, podemos ver um pico seguido por uma queda acentuada, indicando a reação do mercado à crise.

        :red-background[(2) **Março de 2011**] - **Primavera Árabe:**
        A Primavera Árabe, uma série de protestos e revoluções no Oriente Médio e Norte da África, causou incerteza no fornecimento de petróleo, resultando em um aumento dos preços. O gráfico mostra um aumento no preço do petróleo Brent durante esse período.
        \n\n
        :red-background[(3) **Novembro de 2014**] - **OPEP não corta produção, preço cai:**
        Em 2014, a OPEP decidiu não cortar a produção de petróleo, apesar do excesso de oferta no mercado. Essa decisão levou a uma queda significativa nos preços, como indicado pela forte queda observada no gráfico após o evento.
        \n\n
        :red-background[(4) **Janeiro de 2016**] - **Acordo de Corte da OPEP:**
        O acordo de corte de produção pela OPEP em 2016 visava estabilizar os preços do petróleo. No gráfico, podemos observar uma recuperação gradual dos preços após o anúncio do acordo.
        \n\n
        :red-background[(5) **Maio de 2018**] - **EUA saem do acordo nuclear com Irã:**
        A saída dos EUA do acordo nuclear com o Irã aumentou as tensões no Oriente Médio e levou a preocupações sobre a oferta de petróleo, resultando em um aumento dos preços. Isso é refletido no gráfico com um aumento no preço do Brent.
        \n\n
        :red-background[(6) **Março de 2020**] - **Pandemia de COVID-19:**
        A pandemia de COVID-19 causou uma queda drástica na demanda por petróleo devido às restrições de mobilidade e à desaceleração econômica global. O gráfico mostra uma queda acentuada no preço do Brent durante este período.
        \n\n
        :red-background[(7) **Fevereiro de 2022**] - **Invasão da Ucrânia pela Rússia:**
        A invasão da Ucrânia pela Rússia elevou as preocupações sobre a oferta de energia na Europa, resultando em um aumento significativo nos preços do petróleo. O gráfico ilustra um pico nos preços do Brent após o início do conflito.
        \n\n
        :red-background[(8) **Fevereiro de 2023**] - **Tensões no Oriente Médio:**
        As tensões renovadas no Oriente Médio em 2023 novamente impactaram os preços do petróleo, refletindo a sensibilidade do mercado a eventos geopolíticos na região. No gráfico, pode-se observar um aumento nos preços do Brent associado a este evento.
        \n\n
        Esses eventos mostram como fatores externos e decisões políticas podem ter impactos significativos e imediatos nos preços do petróleo, influenciando o mercado global de energia.
    """)

def contet():
    st.markdown("""
    A estratégia utilizada para gerar a previsão do preço do Petróleo Brent neste projeto envolveu a aplicação de vários modelos de machine learning em uma técnica chamada stacking. O stacking é uma técnica de ensemble que combina as previsões de múltiplos modelos base para formar um modelo de nível superior, também conhecido como meta-modelo. Essa abordagem pode melhorar a precisão da previsão, pois cada modelo base pode capturar diferentes padrões nos dados.

    ### Modelos Utilizados

    :gray-background[**K-Nearest Neighbors (KNN)**]:
    - Um modelo de aprendizado supervisionado que classifica os dados com base nos pontos de dados mais próximos no espaço de características.
    - Simples e eficaz, especialmente em problemas onde a relação entre as características e o alvo é complexa.

    :gray-background[**Support Vector Machine (SVM)**]:
    - Um modelo de classificação e regressão que encontra o hiperplano que maximiza a margem entre as classes.
    - Eficaz em espaços de alta dimensionalidade e em casos onde a separação entre classes não é linear.

    :gray-background[**XGBoost**]:
    - Um poderoso algoritmo de boosting baseado em árvores.
    - Otimiza a função de perda através do treinamento sequencial de árvores, onde cada árvore corrige os erros das árvores anteriores.
    - É conhecido por sua alta performance e capacidade de lidar com grandes conjuntos de dados.

    :gray-background[**Bayesian Ridge Regression**]:
    - Uma forma de regressão linear que utiliza inferência Bayesiana para determinar a distribuição dos coeficientes.
    - Inclui um termo de regularização para evitar o overfitting, similar à Ridge Regression.

    :gray-background[**Multi-Layer Perceptron (MLP)**]:
    - Uma rede neural feedforward que consiste de múltiplas camadas de neurônios.
    - Capaz de capturar relações complexas e não lineares nos dados.

    :gray-background[**Meta-modelo (Lasso Regression)**]:
    - Um modelo de regressão linear com regularização L1.
    - O Lasso (Least Absolute Shrinkage and Selection Operator) penaliza o valor absoluto dos coeficientes, forçando alguns coeficientes a zero, o que pode resultar em um modelo mais simples e interpretável.

    ### Geração de Features

    Para treinar os modelos, foram geradas várias características (features) a partir dos dados históricos do preço do petróleo Brent. Essas características incluíram informações temporais, médias móveis, volatilidade e outras estatísticas derivadas dos preços históricos. A criação dessas features foi essencial para fornecer aos modelos informações ricas e relevantes, permitindo que capturassem padrões importantes nos dados.

    ### Processo

    1. **Extração e Preparação dos Dados**: Os dados históricos do preço do Petróleo Brent foram coletados e separados em 3 conjuntos: treinamento da Base, Treinamento do Meta-Modelo e teste.
    2. **Treinamento dos Modelos Base**: Os modelos bases (KNN, SVM, XGBoost, Bayesian Ridge, e MLP) foram treinados usando as features criadas e presentes no primeiro conjunto de teste. A performance e tunnig de cada modelo foi avaliada usando validação cruzada e Grid Search.
    3. **Previsões dos Modelos Base**: Com os modelos treinados foram geradas previsões para o segundo conjunto de treino (Treinamento do Meta-Modelo). Esse conjunto também continha as features criadas.
    4. **Treinamento do Meta-modelo**: O meta-modelo de regressão Lasso, foi treinado no segundo conjunto de teste, utilizando as previsões dos modelos base como parte das features.
    5. **Previsão Final**: O meta-modelo produziu a previsão final combinando as saídas dos modelos base.

    Essa abordagem de stacking permitiu utilizar a força de diferentes algoritmos de machine learning, resultando em uma previsão mais robusta do preço do Petróleo Brent.
    
    """)

def header():
    st.markdown("# Tech Challenge: :red[Petróleo Brent]")
    st.markdown(
        ":gray-background[Tech Challenge] é o projeto final de fase da **PósTech**, ele engloba os conhecimentos obtidos em todas as disciplinas vistas até aquele momento."
    )
    st.markdown(
        """
        **Contexto:**
        Você foi contratado(a) para uma consultoria, e seu trabalho envolve analisar os dados de preço do petróleo brent. Um grande cliente do segmento pediu para que a consultoria desenvolvesse um dashboard interativo e que gere insights relevantes para tomada de decisão. Além disso, solicitaram que fosse desenvolvido um modelo de Machine Learning para fazer o forecasting do preço do petróleo.
    """
    )
    st.markdown(
        """
        <p style="font-size: 14px; color: #AAA; ">
        Projeto criado por <b>Fabricio Zillig</b>. O código fonte está disponível no <a style='color: #999' target='_blank' href='https://github.com/z-fab/postech-data-analytics/tree/master/tech-challenge/f4-brent-oil'>GitHub</a>
        </p>""", unsafe_allow_html=True
    )