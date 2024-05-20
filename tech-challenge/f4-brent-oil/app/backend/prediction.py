from services import Database
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta

db = Database()

def calculate_RSI(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    RS = gain / loss
    return 100 - (100 / (1 + RS))

def calculate_MACD(series, short_period=12, long_period=26, signal_period=9):
    short_ema = series.ewm(span=short_period, adjust=False).mean()
    long_ema = series.ewm(span=long_period, adjust=False).mean()
    macd = short_ema - long_ema
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def calculate_EMA(series, span=20):
    return series.ewm(span=span, adjust=False).mean()

def calculate_ADX(df, window=7):
    high = df['high']
    low = df['low']
    close = df['close']
    
    plus_dm = high.diff()
    minus_dm = low.diff()
    
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm > 0] = 0
    
    tr1 = pd.DataFrame(high - low)
    tr2 = pd.DataFrame(abs(high - close.shift(1)))
    tr3 = pd.DataFrame(abs(low - close.shift(1)))
    tr = pd.concat([tr1, tr2, tr3], axis=1, join='inner').max(axis=1)
    
    atr = tr.rolling(window).mean()
    plus_di = 100 * (plus_dm.ewm(alpha=1/window).mean() / atr)
    minus_di = abs(100 * (minus_dm.ewm(alpha=1/window).mean() / atr))
    
    dx = (abs(plus_di - minus_di) / abs(plus_di + minus_di)) * 100
    adx = dx.rolling(window=window).mean()
    return adx

def prepare_data(last_days):
    df = pd.DataFrame(last_days, columns=['id', 'date', 'close', 'open', 'high', 'low', 'volume']).sort_values('date', ascending=True)
    df.drop(columns=['id'], inplace=True)

    df['RSI'] = calculate_RSI(df['close'], period=7)
    df['MACD'], df['MACD_signal'], df['MACD_hist'] = calculate_MACD(df['close'], short_period=2, long_period=7, signal_period=3)
    df['EMA'] = calculate_EMA(df['close'], span=7)
    df['ADX'] = calculate_ADX(df, window=7)

    df['rolling_mean'] = df['close'].rolling(7).mean()
    df['rolling_std'] = df['close'].rolling(7).std()
    df['rolling_min'] = df['close'].rolling(7).min()
    df['rolling_max'] = df['close'].rolling(7).max()
    df['lag_1'] = df['close'].shift(1)
    df['lag_2'] = df['close'].shift(2)
    df['lag_3'] = df['close'].shift(3)

    return df[df['date'] == df['date'].max()]

def run_prediction(df, id_predict = None):

    BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR = os.path.join(BACKEND_DIR, 'model')

    dict_model = joblib.load(os.path.join(MODEL_DIR, 'models-f4.joblib'))

    X_predict_models = df[dict_model['col_models']].copy()
    X_predict_models_scaled = dict_model['scaler'].transform(X_predict_models)

    knn_predict = dict_model['models']['knn'].predict(X_predict_models_scaled)
    svm_predict = dict_model['models']['svm'].predict(X_predict_models_scaled)
    xgb_predict = dict_model['models']['xgb'].predict(X_predict_models)
    br_predict = dict_model['models']['br'].predict(X_predict_models_scaled)
    mlp_predict = dict_model['models']['mlp'].predict(X_predict_models_scaled)

    X_predict_meta = df.copy()
    X_predict_meta['knn'] = knn_predict
    X_predict_meta['svm'] = svm_predict
    X_predict_meta['xgb'] = xgb_predict
    X_predict_meta['br'] = br_predict
    X_predict_meta['mlp'] = mlp_predict

    meta_predict = dict_model['meta_model'].predict(X_predict_meta[dict_model['col_meta']])
    if id_predict is not None:
        db.insert_prediction(id_predict, meta_predict[0], 'meta')
        db.insert_prediction(id_predict, knn_predict[0], 'knn')
        db.insert_prediction(id_predict, svm_predict[0], 'svm')
        db.insert_prediction(id_predict, xgb_predict[0], 'xgb')
        db.insert_prediction(id_predict, br_predict[0], 'br')
        db.insert_prediction(id_predict, mlp_predict[0], 'mlp')
    else:
        db.insert_next_prediction(meta_predict[0], 'meta')
        db.insert_next_prediction(knn_predict[0], 'knn')
        db.insert_next_prediction(svm_predict[0], 'svm')
        db.insert_next_prediction(xgb_predict[0], 'xgb')
        db.insert_next_prediction(br_predict[0], 'br')
        db.insert_next_prediction(mlp_predict[0], 'mlp')

def load_6m_predictions():
    hist_oil = db.get_range_brent_oil('2024-01-01', datetime.now().strftime('%Y-%m-%d'))
    for register in hist_oil:
        min_date = (register[1] - timedelta(days=21)).strftime('%Y-%m-%d')
        max_date = (register[1] - timedelta(days=1)).strftime('%Y-%m-%d')
        id_predict = register[0]

        print(f"Predicting {id_predict} {register[1]} - {min_date} - {max_date}")
        data_train = db.get_range_brent_oil(min_date, max_date)
        df = prepare_data(data_train)
        run_prediction(df, id_predict)

def predict():
    if db.get_num_predictions() is None or db.get_num_predictions() < 10:
        print("Inserting 6m predictions")
        load_6m_predictions()

    df = prepare_data(db.get_last_days(days = 14))
    run_prediction(df)