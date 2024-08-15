import polars as pl
from sklearn.ensemble import RandomForestClassifier
import pickle


def predict(df: pl.DataFrame):
    dict_model = pickle.load(open("backend/model/model.pkl", "rb"))

    model: RandomForestClassifier = dict_model["model"]
    X = df.select(dict_model["cols"])

    y_proba = model.predict_proba(X)

    return y_proba[0]
