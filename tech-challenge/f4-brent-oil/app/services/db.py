import sqlalchemy
import os

class Database:

    def __init__(self):
        self.__engine = sqlalchemy.create_engine(
            f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
        )

    def get_engine(self):
        return self.__engine
    
    def get_last_brent_oil_date(self):
        with self.__engine.connect() as conn:
            query = sqlalchemy.text("SELECT date FROM brent_oil ORDER BY date DESC LIMIT 1")
            result = conn.execute(query).fetchone()
            return result[0] if result else None

    def get_num_predictions(self):
        with self.__engine.connect() as conn:
            query = sqlalchemy.text("SELECT COUNT(*) FROM prediction")
            result = conn.execute(query).fetchone()
            return result[0] if result else None

    def get_next_id(self):
        with self.__engine.connect() as conn:
            query = sqlalchemy.text("SELECT id FROM brent_oil ORDER BY id DESC LIMIT 1")
            result = conn.execute(query).fetchone()
            return result[0]+1 if result else None

    def insert_brent_oil(self, date, close, open, high, low, volume):
        with self.__engine.connect() as conn:
            query = sqlalchemy.text(f"""
                INSERT INTO brent_oil
                (date, close, open, high, low, volume) 
                VALUES 
                ('{date}', {close}, {open}, {high}, {low}, {volume})
            """)
            conn.execute(query)
            conn.commit()
            print(f"Inserted {date} - {close}")

    def insert_next_prediction(self, prediction, model = 'meta'):
        new_id = self.get_next_id()
        return self.insert_prediction(new_id, prediction, model)

    def insert_prediction(self, id_prediction, prediction, model = 'meta'):
        with self.__engine.connect() as conn:

            query = sqlalchemy.text(f"SELECT * FROM prediction WHERE id = '{id_prediction}' and model = '{model}'")
            result = conn.execute(query).fetchone()
            if result:
                print(f"Prediction {id_prediction} - {model} already exists!")
                return None

            query = sqlalchemy.text(f"INSERT INTO prediction (id, value, model) VALUES ('{id_prediction}', {prediction}, '{model}')")
            conn.execute(query)
            conn.commit()
        print(f"Inserted prediction {id_prediction} - {prediction}")
        return id_prediction

    def get_last_days(self, days = 7):
        with self.__engine.connect() as conn:
            query = sqlalchemy.text(f"SELECT * FROM brent_oil ORDER BY date DESC LIMIT {days}")
            result = conn.execute(query)
            return result.fetchall()

    def get_range_brent_oil(self, start, end):
        with self.__engine.connect() as conn:
            query = sqlalchemy.text(f"SELECT * FROM brent_oil WHERE date >= '{start}' AND date <= '{end}'")
            result = conn.execute(query)
            return result.fetchall()

    def get_all_brent_prediciton(self):
        with self.__engine.connect() as conn:
            query = sqlalchemy.text(f"""
                SELECT * FROM brent_oil AS t1
                INNER JOIN prediction AS t2 ON t1.id = t2.id
            """)
            result = conn.execute(query)
            return result.fetchall()

    def get_last_prediction(self):
        with self.__engine.connect() as conn:
            query = sqlalchemy.text(f"""
                SELECT * FROM prediction WHERE id = (SELECT MAX(id) FROM prediction)
            """)
            result = conn.execute(query)
            return result.fetchall()

    def get_all_brent_oil(self):
        with self.__engine.connect() as conn:
            query = sqlalchemy.text(f"""
                SELECT * FROM brent_oil
            """)
            result = conn.execute(query)
            return result.fetchall()
            
