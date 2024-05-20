from services import Database
import yfinance as yf

db = Database()

def fetch_brent_oil_history():
    brent = yf.Ticker("BZ=F")
    hist = brent.history(period="max")
    return hist

def fetch_latest_brent_oil():

    brent = yf.Ticker("BZ=F")
    hist = brent.history(period="10d")
    last_date = hist.index.max().date()
    last_close = hist.iloc[-1]['Close']
    last_open = hist.iloc[-1]['Open']
    last_high = hist.iloc[-1]['High']
    last_low = hist.iloc[-1]['Low']
    last_volume = hist.iloc[-1]['Volume']

    return last_date, last_close, last_open, last_high, last_low, last_volume

def update_database():
    last_date = db.get_last_brent_oil_date()
    if last_date == None:
        print("Inserting all data")
        hist = fetch_brent_oil_history()
        for date, row in hist.iterrows():
            db.insert_brent_oil(
                date.date(), 
                row['Close'],
                row['Open'],
                row['High'],
                row['Low'],
                row['Volume']
            )
    else:
        date, close, open, high, low, volume = fetch_latest_brent_oil()
        if last_date < date:
            print(f"Inserting {date} - {close}")
            db.insert_brent_oil(date, close, open, high, low, volume)
            return True
        print("No new data to insert")
        return False

def sync():
    update_database()
    