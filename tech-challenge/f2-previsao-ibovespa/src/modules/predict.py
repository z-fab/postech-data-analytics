import logging
import pandas as pd
from pmdarima import auto_arima

from .models import PredictIbovespa

logger = logging.getLogger("f2-log")


class Predictor:
    def __init__(self, data_raw, last_date=None):
        self.df = self._preprocessing(data_raw, last_date)

    def _preprocessing(self, data, last_date=None):
        logger.info("Iniciando pré-processamento dos dados")

        df = pd.DataFrame(data)
        df = df[["date", "close"]]
        df.rename(columns={"close": "y", "date": "ds"}, inplace=True)

        if last_date is not None:
            pd_last_date = pd.DataFrame({"ds": [last_date], "y": [None]})
            df = pd.concat([df, pd_last_date], ignore_index=True, axis=0)

        df["ds"] = pd.to_datetime(df["ds"])
        df = df.sort_values(by=["ds"])

        ds_min = df["ds"].min().date()
        ds_max = df["ds"].max().date()

        df.set_index("ds", inplace=True)
        df = df.asfreq("D")
        df = df.ffill()

        logger.info(
            "Pré-processamento finalizado. Total de registros: %s [Inicio %s : Fim %s]",
            len(df),
            ds_min,
            ds_max,
        )
        return df

    def getDataFrame(self):
        return self.df

    def predict(self, n_periods=3):
        logger.info("Iniciando predição")
        model_arima = auto_arima(
            self.df,
            seasonal=True,
            trace=False,
            error_action="ignore",
            suppress_warnings=True,
        )
        predict = model_arima.predict(n_periods=n_periods)

        list_predict = []
        for p in predict.reset_index().iterrows():
            predict = PredictIbovespa(
                date=p[1]["index"].strftime("%Y-%m-%d"), predict=p[1][0]
            )
            logger.info("Objeto de predição criado: %s", predict.__dict__)
            list_predict.append(predict)

        logger.info("Predição finalizada.")

        return list_predict
