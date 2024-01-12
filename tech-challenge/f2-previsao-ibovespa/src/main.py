import datetime
import os
import time
import schedule

import logging
import logging.handlers as handlers

from modules.database import Database
from modules.collector import BovespaCollector
from modules.predict import Predictor
from modules.models import Consolidate


# Definindo variáveis de ambiente com os caminhos dos diretórios
PATHS = {}
PATHS['SRC_DIR'] = os.path.dirname(__file__)
PATHS['BASE_DIR'] = os.path.dirname(PATHS['SRC_DIR'])
PATHS['DATA_DIR'] = os.path.join(PATHS['BASE_DIR'], 'data')
PATHS['LOG_DIR'] = os.path.join(PATHS['BASE_DIR'], 'log')

for key, value in PATHS.items():
    os.environ[key] = value

# Criando configuracao de logging
logger = logging.getLogger('f2-log')
logger.setLevel(logging.DEBUG)

c_handler = logging.StreamHandler()
c_handler.setLevel(logging.DEBUG)
c_format = logging.Formatter('%(asctime)s :: (%(name)s | %(filename)s) %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
logger.addHandler(c_handler)

f_handler = handlers.TimedRotatingFileHandler(f"{PATHS['LOG_DIR']}/f2.log", when="midnight", backupCount=15)
f_handler.suffix = "%Y%m%d"
f_handler.setLevel(logging.INFO)
f_format = logging.Formatter('%(asctime)s :: (%(name)s | %(filename)s) %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


def ingestion():
    logger.info("\n[ INICIANDO PROCESSO DE INGESTÃO ]\n")

    db = Database(path = os.path.join(os.getenv('DATA_DIR'), 'ibovespa.db'))

    last_date = db.getLastDateIbov()
    yesterday = datetime.datetime.now().date() - datetime.timedelta(days=1)

    # Se não houver dados no banco de dados, coletar a partir de 01/01/2023
    if last_date is None:
        last_date = datetime.date(2000, 1, 1)
        logger.info(f'Não há dados no banco de dados, coletando a partir de {last_date}')

    # Se a última data no Banco for maior ou igual a ontem, não há necessidade de coletar novos dados
    elif last_date >= yesterday:
        logger.info('Não há novos dados para serem coletados')
        return None

    # Se a última data no Banco for menor que ontem, coletar a partir do dia seguinte
    else:
        last_date = last_date + datetime.timedelta(days=1)
        logger.info('Coletando dados a partir de %s', last_date)

    data_ibovespa = BovespaCollector().get_data(start_date=last_date)

    # Se não houver dados para serem salvos no banco de dados, não há necessidade de salvar
    if data_ibovespa is None or len(data_ibovespa) <= 0:
        logger.info('Nenhum dado para ser salvo no banco de dados')
        return None
    
    # Salvando dados no banco de dados
    db.insertIbov(data_ibovespa)

    logger.info("\n[ INGESTÃO FINALIZADA ]\n")

    return None


def predict():

    logger.info("\n[ INICIANDO PROCESSO DE PREDIÇÃO ]\n")

    db = Database(path = os.path.join(os.getenv('DATA_DIR'), 'ibovespa.db'))
    
    # Verificando a última data de predição. Caso não haja, iniciar a partir de 01/06/2023
    lastDatePredicted = db.getLastDatePred()
    lastDatePredicted = lastDatePredicted if lastDatePredicted is not None else datetime.date(2023, 6, 1)
    
    lastDateIbov = db.getLastDateIbov()

    # Se a última data de predição for maior que a última data que temos do Ibovespa, não há necessidade de novas predições
    if lastDatePredicted > lastDateIbov:
        logger.info('Última data de predição: %s. Não há necessidade de novas predições', lastDatePredicted)
        return None

    logger.info('Última data de predição: %s. Realizando predições!', lastDatePredicted)

    # Coletando dados do Ibovespa para realizar a predição
    data_ibovespa = db.getDataIbov(
        start_date=lastDatePredicted - datetime.timedelta(days=90), 
        end_date=lastDatePredicted
    )

    lastDateReturn = data_ibovespa[-1][0]
    lastDateReturn = datetime.datetime.strptime(lastDateReturn, '%Y-%m-%d').date()
    print(lastDateReturn >= lastDatePredicted)

    if lastDateReturn >= lastDatePredicted:
        pred = Predictor(data_ibovespa).predict()
    else:  
        pred = Predictor(data_ibovespa, last_date=lastDatePredicted).predict()

    db.insertPredict(pred)

    predict()

    logger.info("\n[ PREDIÇÃO FINALIZADA ]\n")

    return None



def consolidate():

    logger.info("\n[ INICIANDO PROCESSO DE CONSOLIDATE ]\n")

    db = Database(path = os.path.join(os.getenv('DATA_DIR'), 'ibovespa.db'))
    start_date = datetime.date(2023, 1, 1)
    end_date = db.getLastDatePred()

    # Se não houver dados de predição usaremos como data final a última data do Ibovespa
    if end_date is None:
        end_date = db.getLastDateIbov()
        logger.info('Não há dados de predição. Usando Ibovespa como data final: %s', end_date)

    # Criando lista de objetos Consolidate
    list_consolidate = []

    # Loop para gerar os objetos Consolidate.
    while start_date <= end_date:

        pred = db.getDataPred(start_date=start_date, end_date=start_date)
        ibov = db.getDataIbov(start_date=start_date, end_date=start_date)

        # Se não houver dados de predição ou Ibovespa, preencher com 0
        if pred is None:
            pred = 0
        else:
            pred = pred[0][-1]
        
        if ibov is None:
            ibov = 0
        else:
            ibov = ibov[0][-1]

        # Criando objeto Consolidate
        consolidate = Consolidate(
            date = start_date,
            close = ibov,
            predict = pred
        )
        list_consolidate.append(consolidate)

        # Incrementando data em 1 dia
        start_date = start_date + datetime.timedelta(days=1)

    db.insertConsolidate(list_consolidate)

    logger.info("\n[ CONSOLIDATE FINALIZADA ]\n")

    return None

def main():
    
    ingestion()
    predict()
    consolidate()


if __name__ == '__main__':
    
    main()
    schedule.every().day.at("06:00").do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)

