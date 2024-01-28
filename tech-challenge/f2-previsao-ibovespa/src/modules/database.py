import logging
import datetime
import os
import sqlalchemy as db

from .models import IBovespaData
from .models import PredictIbovespa

logger = logging.getLogger("f2-log")


class Database:
    def __init__(self, path: str = None):
        if not path:
            path = os.path.join(os.path.dirname(__file__), "ibovespa.db")
        self.engine = db.create_engine("sqlite:///" + path)
        self._create_tables()

    def _create_tables(self):
        query_ibovespa = """
            CREATE TABLE IF NOT EXISTS ibovespa (
                date DATE PRIMARY KEY,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT
            );
        """
        query_predict = """
            CREATE TABLE IF NOT EXISTS predict (
                date DATE PRIMARY KEY,
                predict FLOAT
            );
        """

        query_consolidate = """
            CREATE TABLE IF NOT EXISTS consolidate (
                date DATE PRIMARY KEY,
                close FLOAT,
                predict FLOAT,
                diff FLOAT,
                diff_percent FLOAT
            );
        """

        with self.engine.connect() as conn:
            conn.execute(db.text(query_ibovespa))
            conn.execute(db.text(query_predict))
            conn.execute(db.text(query_consolidate))

    def getLastDateIbov(self):
        query = """
            SELECT date FROM ibovespa ORDER BY date DESC LIMIT 1;
        """

        with self.engine.connect() as conn:
            result = conn.execute(db.text(query)).all()
            logger.debug("Última data do Ibovespa no banco de dados: %s", result)
            if len(result) <= 0:
                return None
            return datetime.datetime.strptime(result[0][0], "%Y-%m-%d").date()

    def getLastDatePred(self):
        query = """
            SELECT date FROM predict ORDER BY date DESC LIMIT 1;
        """

        with self.engine.connect() as conn:
            result = conn.execute(db.text(query)).all()
            logger.debug("Última data de predição no banco de dados: %s", result)
            if len(result) <= 0:
                return None
            return datetime.datetime.strptime(result[0][0], "%Y-%m-%d").date()

    def getLastDateConsolidate(self):
        query = """
            SELECT date FROM consolidate ORDER BY date DESC LIMIT 1;
        """

        with self.engine.connect() as conn:
            result = conn.execute(db.text(query)).all()
            logger.debug("Última data consolidada no banco de dados: %s", result)
            if len(result) <= 0:
                return None
            return datetime.datetime.strptime(result[0][0], "%Y-%m-%d").date()

    def getDataIbov(
        self, start_date=None, end_date=datetime.datetime.now().strftime("%Y-%m-%d")
    ):
        if not start_date:
            query = """
                SELECT * FROM ibovespa;
            """
        else:
            query = """
                SELECT * FROM ibovespa WHERE date BETWEEN :start_date AND :end_date;
            """

        with self.engine.connect() as conn:
            result = conn.execute(
                db.text(query), {"start_date": start_date, "end_date": end_date}
            )
            data = result.fetchall()
            if data:
                logger.info(
                    "Retornando %s registros do banco de dados [ Start %s | End %s ]",
                    len(data),
                    data[0][0],
                    data[-1][0],
                )
                return data
            else:
                logger.info(
                    "Nenhum dado retornado do banco de dados [ Start %s | End %s ]",
                    start_date,
                    end_date,
                )
                return None

    def getDataPred(
        self, start_date=None, end_date=datetime.datetime.now().strftime("%Y-%m-%d")
    ):
        if not start_date:
            query = """
                SELECT * FROM predict;
            """
        else:
            query = """
                SELECT * FROM predict WHERE date BETWEEN :start_date AND :end_date;
            """

        with self.engine.connect() as conn:
            result = conn.execute(
                db.text(query), {"start_date": start_date, "end_date": end_date}
            )
            data = result.fetchall()
            if data:
                logger.info(
                    "Retornando %s registros de predict [ Start %s | End %s ]",
                    len(data),
                    start_date,
                    end_date,
                )
                return data
            else:
                logger.info(
                    "Nenhum dado retornado de predict [ Start %s | End %s ]",
                    start_date,
                    end_date,
                )
                return None

    def getDataConsolidate(self, h=7):
        query = """
            SELECT * FROM consolidate ORDER BY date DESC LIMIT :h;
        """

        with self.engine.connect() as conn:
            result = conn.execute(db.text(query), {"h": h})
            data = result.fetchall()
            if data:
                logger.info("Retornando %s registros de predict [ H %s ]", len(data), h)
                return data
            else:
                logger.info("Nenhum dado retornado de predict [ H %s ]", h)
                return None

    def insertIbov(self, data):
        if data is None:
            return None

        query = """
            INSERT INTO ibovespa 
                (date, open, high, low, close) 
            VALUES
                (:date, :open, :high, :low, :close);
        """
        try:
            with self.engine.connect() as conn:
                if isinstance(data, list):
                    logger.info("Inserindo %s registros em IBovespa", len(data))
                    for ibov in data:
                        logger.info("Inserindo registro de %s em IBovespa", ibov.date)
                        conn.execute(
                            db.text(query),
                            {
                                "date": ibov.date,
                                "open": ibov.open,
                                "high": ibov.high,
                                "low": ibov.low,
                                "close": ibov.close,
                            },
                        )
                else:
                    logger.info("Inserindo registro de %s em IBovespa", data.date)
                    conn.execute(
                        db.text(query),
                        {
                            "date": data.date,
                            "open": data.open,
                            "high": data.high,
                            "low": data.low,
                            "close": data.close,
                        },
                    )
                conn.commit()
        except Exception as e:
            logger.error("Erro ao inserir dados na tabela Ibovespa: %s", e)

    def insertPredict(self, data):
        if data is None:
            return None

        query = """
            INSERT INTO predict 
                (date, predict) 
            VALUES
                (:date, :predict);
        """
        try:
            with self.engine.connect() as conn:
                if isinstance(data, list):
                    logger.info("Inserindo %s registros em Predict", len(data))
                    for pred in data:
                        logger.info("Inserindo registro de %s em Predict", pred.date)
                        conn.execute(
                            db.text(query),
                            {
                                "date": pred.date,
                                "predict": pred.predict,
                            },
                        )
                else:
                    logger.info("Inserindo registro de %s em Predict", data.date)
                    conn.execute(
                        db.text(query), {"date": pred.date, "predict": pred.predict}
                    )
                conn.commit()
        except Exception as e:
            logger.error("Erro ao inserir dados  na tabela Predict: %s", e)

    def insertConsolidate(self, data):
        if data is None:
            return None

        query_exclude = """
            DELETE FROM consolidate;
        """

        query = """
            INSERT INTO consolidate 
                (date, close, predict, diff, diff_percent) 
            VALUES
                (:date, :close, :predict, :diff, :diff_percent);
        """
        try:
            with self.engine.connect() as conn:
                logger.info("Excluindo registros da tabela Consolidate")
                conn.execute(db.text(query_exclude))
                conn.commit()

                if isinstance(data, list):
                    logger.info("Inserindo %s registros em Consolidate", len(data))
                    for consolidate in data:
                        logger.info(
                            "Inserindo registro de %s em Consolidate", consolidate.date
                        )
                        conn.execute(
                            db.text(query),
                            {
                                "date": consolidate.date,
                                "close": consolidate.close,
                                "predict": consolidate.predict,
                                "diff": consolidate.diff,
                                "diff_percent": consolidate.diff_percent,
                            },
                        )
                else:
                    logger.info("Inserindo registro de %s em Consolidate", data.date)
                    conn.execute(
                        db.text(query),
                        {
                            "date": consolidate.date,
                            "close": consolidate.close,
                            "predict": consolidate.predict,
                            "diff": consolidate.diff,
                            "diff_percent": consolidate.diff_percent,
                        },
                    )
                conn.commit()
        except Exception as e:
            logger.error("Erro ao inserir dados na tabela Consolidate: %s", e)
