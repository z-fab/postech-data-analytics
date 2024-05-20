# Tech Challenge - Fase 4 🛢️

_Tech Challenge é o projeto final de fase da PósTech, ele engloba os conhecimentos obtidos em todas as disciplinas vistas até aquele momento._

### Contexto

Você foi contratado(a) para uma consultoria, e seu trabalho envolve analisar os dados de preço do petróleo brent. Um grande cliente do segmento pediu para que a consultoria desenvolvesse um dashboard interativo e que gere insights relevantes para tomada de decisão. Além disso, solicitaram que fosse desenvolvido um modelo de Machine Learning para fazer o forecasting do preço do petróleo.

## Resultado:

>Dashboard: [https://postech.zfab.me/tcf4](https://postech.zfab.me/tcf4)

A estratégia utilizada para gerar a previsão do preço do Petróleo Brent neste projeto envolveu a aplicação de vários modelos de machine learning em uma técnica chamada stacking. O stacking é uma técnica de ensemble que combina as previsões de múltiplos modelos base para formar um modelo de nível superior, também conhecido como meta-modelo. Essa abordagem pode melhorar a precisão da previsão, pois cada modelo base pode capturar diferentes padrões nos dados.

### Modelos Utilizados

**K-Nearest Neighbors (KNN)**:
- Um modelo de aprendizado supervisionado que classifica os dados com base nos pontos de dados mais próximos no espaço de características.
- Simples e eficaz, especialmente em problemas onde a relação entre as características e o alvo é complexa.

**Support Vector Machine (SVM)**:
- Um modelo de classificação e regressão que encontra o hiperplano que maximiza a margem entre as classes.
- Eficaz em espaços de alta dimensionalidade e em casos onde a separação entre classes não é linear.

**XGBoost**:
- Um poderoso algoritmo de boosting baseado em árvores.
- Otimiza a função de perda através do treinamento sequencial de árvores, onde cada árvore corrige os erros das árvores anteriores.
- É conhecido por sua alta performance e capacidade de lidar com grandes conjuntos de dados.

**Bayesian Ridge Regression**:
- Uma forma de regressão linear que utiliza inferência Bayesiana para determinar a distribuição dos coeficientes.
- Inclui um termo de regularização para evitar o overfitting, similar à Ridge Regression.

**Multi-Layer Perceptron (MLP)**:
- Uma rede neural feedforward que consiste de múltiplas camadas de neurônios.
- Capaz de capturar relações complexas e não lineares nos dados.

**Meta-modelo (Lasso Regression)**:
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
