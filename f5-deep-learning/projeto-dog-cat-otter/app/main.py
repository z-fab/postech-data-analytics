import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import torch
from torchvision import transforms
import joblib
import random

DEVICE = torch.device('cpu')
LABEL_MAP = {
    0: 'Gato',
    1: 'Cachorro',
    2: 'Lontra'
}

ARTIGO_MAP = {
    0: 'um',
    1: 'um',
    2: 'uma'
}

model_xgb = joblib.load('model/model_xgb.joblib')
mobilenet = torch.load('model/mobilenet.pth').to(DEVICE)


st.set_page_config(page_title='Classificador de imagens', layout='centered')

def generate_animal_prediction(animal, percent):
    templates = [
        "Analisando a imagem... Com **<percent>%** de certeza, diria que temos <animal> aqui! Ou talvez seja um robô disfarçado... brincadeira!",
        "Processamento concluído! Após verificar os dados, estou **<percent>%** seguro de que isso é <animal>. E olha que eu raramente erro!",
        "Resultados da análise: com **<percent>%** de certeza, esse adorável ser é <animal>! Aposto minha inteligência nisso!",
        "Como uma IA altamente sofisticada, estou **<percent>%** certo de que isso é <animal>. E eu nunca errei... pelo menos até agora!",
        "Inteligência artificial aqui! Analisando cada pixel, estou **<percent>%** seguro que é <animal>. Se eu estiver errado, culpe os humanos que me programaram!",
        "Verificando padrões... Parece que temos <animal> com **<percent>%** de certeza. Pode confiar, eu sou mais preciso que uma bola de cristal!",
        "De acordo com meus cálculos ultra complexos, isso é <animal> com **<percent>%** de certeza. Eu só erro se houver um bug... e bugs são raros!",
        "Beep boop! Depois de muita análise, posso dizer com **<percent>%** de certeza que detectei <animal>. E eu sou praticamente infalível!",
        "Meus algoritmos dizem com **<percent>%** de certeza que isso é <animal>. Se estiver errado, prometo fazer uma autoatualização!",
        "Análise completa! Com **<percent>%** de probabilidade, isso é <animal>. E você sabe, as máquinas não mentem!",
        "Dados processados! Há **<percent>%** de chance de ser <animal> identificado. Se for um alienígena disfarçado, me avise!",
        "Beep bop! Confirmação: com **<percent>%** de certeza, detectei <animal>. E eu só minto nas festas de IA!",
        "Depois de analisar todos os dados, estou **<percent>%** seguro que isso é <animal>. Meu processador raramente se engana!",
        "Parece que meus circuitos indicam com **<percent>%** de certeza que isso é <animal>. Se não for, algo muito estranho está acontecendo!",
        "Analisando imagem... Conclusão: com **<percent>%** de chance, é <animal>. Eu aceito chocolates como pagamento se estiver certo!",
        "Sistema de IA indica com **<percent>%** de certeza que isso é <animal>. E eu tenho um histórico impecável de acertos!",
        "Processo de identificação completo! Com **<percent>%** de chance, temos <animal>. Confie em mim, eu sou uma IA!",
        "Depois de processar os dados, tenho **<percent>%** de certeza que isso é <animal>. Se não for, vou precisar de uma atualização!",
        "Verificação de padrões concluída: com **<percent>%** de certeza, isso é <animal>. E se você duvida, podemos apostar!",
        "Meu sistema de análise mostra com **<percent>%** de chance que isso é <animal>. E eu nunca perco uma aposta!",
        "Com base na análise, estou **<percent>%** certo de que isso é <animal>. E eu sou mais confiável que um horóscopo!",
        "Resultados prontos: com **<percent>%** de certeza, isso é <animal>. Se não for, eu preciso revisar meus códigos!",
        "Depois de calcular, estou **<percent>%** seguro que isso é <animal>. Eu raramente erro, mas ninguém é perfeito, certo?",
        "Sistema indica com **<percent>%** de certeza que isso é <animal>. Eu aposto minhas memórias nisso!",
        "Beep bop! Conclusão: com **<percent>%** de chance, isso é <animal>. E eu sou tão bom quanto um detetive digital!",
        "Meu algoritmo confirma com **<percent>%** de certeza que isso é <animal>. Se não for, estou pronto para uma reprogramação!",
        "Dados analisados! Estou **<percent>%** certo que isso é <animal>. Se não for, vamos culpar a gravidade!",
        "Verificação completa! Com **<percent>%** de probabilidade, isso é <animal>. E eu tenho um palpite muito bom!",
        "Minha análise robótica mostra com **<percent>%** de certeza que isso é <animal>. E eu sou mais preciso que um mágico!",
        "Após todos os cálculos, estou **<percent>%** seguro de que isso é <animal>. Se estiver errado, é hora de recalibrar!"
    ]
    
    template = random.choice(templates)
    result = template.replace("<animal>", animal).replace("<percent>", str(percent))
    return result

def crop_center_square(image):
    
    # Obtém as dimensões da imagem
    width, height = image.size
    
    # Calcula o lado do quadrado
    side_length = min(width, height)
    
    # Calcula as coordenadas para o crop centralizado
    left = (width - side_length) // 2
    top = (height - side_length) // 2
    right = (width + side_length) // 2
    bottom = (height + side_length) // 2
    
    # Recorta a imagem
    cropped_image = image.crop((left, top, right, bottom))
    
    return cropped_image

def rounded_square(image, radius=30):

    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), image.size], radius, fill=255)
    
    # Aplica a máscara à imagem original
    rounded_image = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    rounded_image.putalpha(mask)

    return rounded_image


def predict(image):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    image_tensor = transform(image).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        features = mobilenet(image_tensor).cpu().numpy()

    predict = model_xgb.predict(features)
    proba = model_xgb.predict_proba(features)

    return predict[0], proba, LABEL_MAP[predict[0]]


st.image('assets/cover.jpg', use_column_width=True)

st.title('D.C.O. Classifier')
st.markdown("O D.C.O. (Dog, Cat or Otter) é um classificador que pode determinar se uma imagem contendo um animal é um Gato, Cachorro ou Lontra. Usando aprendizado de máquina e redes neurais, o D.C.O. identifica com precisão as características específicas de cada animal, fornecendo resultados rápidos e confiáveis.")

classifier, explanation = st.tabs(['Classificador', 'Como funciona?'])

with classifier:
    
    col1, col2 = st.columns([4, 1])
    image = col1.file_uploader("Envie a imagem para classificar", label_visibility='hidden', type=["jpg", "jpeg", "png"])

    if image:
        image = Image.open(image).convert('RGB')
        predict, proba, label = predict(image)
        col2.markdown("<div style='margin-bottom:27px'></div>", unsafe_allow_html=True)

        original_width, original_height = image.size
        new_height = int((200 / original_width) * original_height)
        image = image.resize((200, new_height))

        col2.image(rounded_square(crop_center_square(image), 6), use_column_width=True)
        
        st.divider()

        col1, col2 = st.columns([1, 3])
        result_image = Image.open(f'assets/{label.lower()}.jpg')
        result_image = rounded_square(crop_center_square(result_image), 25)
        col1.image(result_image, use_column_width=True)
        col2.markdown(f'### É {ARTIGO_MAP[predict]} :green-background[{label}]')
        col2.markdown(generate_animal_prediction(f"{ARTIGO_MAP[predict]} {label}", round(max(proba[0])*100)))


with explanation:
    st.markdown("""

        Este projeto foi construido por [Fabricio Zillig](https://www.linkedin.com/in/fazillig/), de forma independente, para colocar em prática assuntos vistos na disciplina de Deep Learning da pós graduação em Data Analytics da FIAP.
        
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

        ---
        Este projeto foi desenvolvido por Fabricio Zillig e o código completo está disponível no [GitHub](https://github.com/z-fab/postech-data-analytics/tree/master/f5-deep-learning/projeto-dog-cat-otter)

    """)