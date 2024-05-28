# Classificador DCO - Fase 5 

_Este projeto paralelo foi construido de forma independente para colocar em prática assuntos vistos na Fase 5 da Postech._

### Contexto

Com o objetivo de colocar em prática os conceitos de CNN e Transfer Learning, neste projeto foi desenvolvido um classificador de imagens que identifica se a imagem contém um gato, um cachorro ou uma lontra. 


## Resultado:

> Classificador Online: [https://postech.zfab.me/dco](https://postech.zfab.me/dco)


Este classificador de imagens combina de maneira inteligente técnicas de deep learning e modelos tradicionais de machine learning. A arquitetura utiliza uma rede neural convolucional (CNN) pré-treinada, a MobileNet V3, para extrair características das imagens, seguida por um modelo XGBoost treinado para classificar essas características.

#### Extração de Features com MobileNet V3
Em vez de treinar uma CNN do zero, utilizamos a MobileNet V3, conhecida por sua eficiência e precisão em tarefas de classificação de imagens. Adaptamos essa rede para retornar um vetor de 512 features, extraindo assim as características mais importantes de cada imagem.

#### Classificação com XGBoost
As features extraídas pela MobileNet V3 são passadas para um modelo XGBoost, um algoritmo de boosting baseado em árvores, que foi treinado para classificar as imagens como Gato, Cachorro ou Lontra. Esta abordagem permite utilizar a robustez da MobileNet V3 na extração de características visuais complexas, enquanto aproveitamos a eficácia do XGBoost em tarefas de classificação.

#### Vantagens dessa abordagem
Essa arquitetura, que combina deep learning com machine learning tradicional, apresenta várias vantagens:

- **Eficiência e Velocidade:** 
Não foi necessário treinar uma CNN do zero, economizando recursos computacionais e tempo. A MobileNet V3, já treinada em um grande conjunto de dados de imagens, fornece uma base sólida para a extração de features.

- **Flexibilidade e Acurácia:**
A combinação de deep learning com modelos tradicionais de machine learning, como o XGBoost, mostra que uma pipeline 100% baseada em deep learning não é sempre necessária. Utilizar um modelo de boosting para a classificação final permitiu alcançar uma acurácia notável de 97% nos testes.