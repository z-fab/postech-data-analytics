# Datathon - Fase 5 📚

_Datathon é o projeto final da PósTech, ele engloba os conhecimentos obtidos em todas as disciplinas vistas na pós-graduação_
    

### Contexto

O grande objetivo do datathon é criar uma proposta preditiva para potencializar o impacto que a **ONG Passos Mágicos** tem realizado sobre a comunidade que atende. 
    
## Resultado:

>Dashboard: [https://postech.zfab.me/tcf5](https://postech.zfab.me/tcf5)

Este projeto teve como objetivo desenvolver um modelo de aprendizado de máquina para prever a presença de alunos em aulas futuras.

O modelo se baseia no histórico do diário de classe e em outras informações relevantes sobre as aulas e os estudantes. Para criar uma visão abrangente e robusta, utilizamos dados provenientes de seis bases distintas, que incluem informações sobre cadastro de alunos, professores, turmas e disciplinas.

### Desenvolvimento

O processo de desenvolvimento começou com a coleta e integração dos dados brutos dessas seis tabelas diferentes. Realizamos um trabalho minucioso de agregação para criar um único conjunto de dados coeso e informativo. Este conjunto de dados consolidado foi então utilizado para treinar nosso modelo de aprendizado de máquina.

A estrutura da nossa base de dados é fundamental para o funcionamento do modelo. Cada linha representa um aluno específico e contém informações sobre seu comportamento e características durante as dez aulas anteriores. Essa abordagem nos permite capturar padrões temporais na frequência dos alunos e correlacioná-los com outros fatores relevantes.

Para a modelagem, optamos por utilizar um algoritmo de floresta aleatória, conhecido por sua eficácia em tarefas de classificação e regressão. Este algoritmo nos permite lidar com a complexidade das relações entre as diversas variáveis que influenciam a presença dos alunos.

### Resultados

Como evolução é interessante buscar maneiras de refinar e melhorar o modelo. Isso inclui a exploração de novas features, a experimentação com outros algoritmos e a incorporação de dados adicionais que possam aumentar a precisão de nossas previsões.

O objetivo final é fornecer uma ferramenta valiosa para a organização e professores, permitindo intervenções proativas para melhorar a assiduidade e, consequentemente, o desempenho acadêmico dos estudantes.
    
