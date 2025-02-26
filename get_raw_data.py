import requests
import os
from dataclasses import dataclass
from dotenv import load_dotenv
import datetime
import psycopg2

load_dotenv()
DB_NAME = "postgres"
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_HOST = "localhost"
API_KEY = os.getenv("API_KEY", "DEFAULT")
DATABASE_URL = "postgresql://{}:{}@{}:5433/{}".format(
    DB_USER, DB_PASS, DB_HOST, DB_NAME
)
conn = psycopg2.connect(DATABASE_URL)
today = datetime.datetime.now().strftime("%Y-%m-%d")
prev_date = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime("%Y-%m-%d")
stock_options = ["IBM", "AAPL"]
all_records, res = [], []


@dataclass
class FinancialData:
    symbol: str
    date: str
    open_price: str
    close_price: str
    volume: str


# Get all data from external API
for stock in stock_options:
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={}&apikey={}".format(
        stock, API_KEY
    )
    response = requests.get(url).json()
    symbol = response["Meta Data"]["2. Symbol"]
    for date in response["Time Series (Daily)"].keys():
        valid_date = prev_date <= date <= today
        if valid_date:
            open_price = response["Time Series (Daily)"][date]["1. open"]
            close_price = response["Time Series (Daily)"][date]["4. close"]
            volume = response["Time Series (Daily)"][date]["6. volume"]
            record = [symbol, date, open_price, close_price, volume]
            all_records.append(record)
            res.append(FinancialData(symbol, date, open_price, close_price, volume))

# Insert into database
with conn.cursor() as cur:
    sql = "INSERT INTO financial_data (symbol, date, open_price, close_price, volume) VALUES (%s, %s,%s, %s, %s) ON CONFLICT DO NOTHING;"
    cur.executemany(sql, all_records)

conn.commit()
cur.close()
conn.close()

# Printout output
for record in res:
    print(record)
