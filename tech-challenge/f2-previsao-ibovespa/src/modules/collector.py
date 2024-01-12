import logging
import yfinance as yf
from datetime import datetime
from .models import IBovespaData

logger = logging.getLogger('f2-log')

class BovespaCollector:
   
    def __init__(self, ticker="^BVSP"):
        self.ticker = ticker

    def get_data(self, start_date = '2000-01-01', end_date:str = datetime.now().strftime('%Y-%m-%d')):
        logger.debug('Solicitando dados da API - Start Date: %s - End Date: %s', start_date, end_date)
        data = yf.download(self.ticker, start=start_date, end=end_date)

        bovespa_data_list = []
        if not data.empty:
            for date, row in data.iterrows():
                bovespa_data = IBovespaData(
                    date=date.strftime('%Y-%m-%d'),
                    open=row['Open'],
                    high=row['High'],
                    low=row['Low'],
                    close=row['Close']
                )
                bovespa_data_list.append(bovespa_data)

            return bovespa_data_list
        else:
            logger.info('Nenhum dado retornado pela API')
            return None
