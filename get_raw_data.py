import requests
import os
from dotenv import load_dotenv
import datetime
import psycopg2

load_dotenv()
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
API_KEY = os.getenv("API_KEY", "DEFAULT")
connection = psycopg2.connect(
    host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME
)
today = datetime.datetime.now().strftime("%Y-%m-%d")
prev_date = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime("%Y-%m-%d")
stock_options = ["IBM", "AAPL"]
all_records = []

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

# Insert into database
with connection:
    with connection.cursor() as cursor:
        sql = "INSERT INTO financial_data (symbol, date, open_price, close_price, volume) VALUES (%s, %s,%s, %s, %s) ON CONFLICT DO NOTHING;"
        try:
            cursor.executemany(sql, all_records)
        except Exception as E:
            print(E)
    connection.commit()
cursor.close()
connection.close()
