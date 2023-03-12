import os
from dataclasses import dataclass
from dotenv import load_dotenv
import psycopg2
from fastapi import APIRouter, HTTPException
import datetime
import logging

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)
load_dotenv()
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DEFAULT_SYMBOL = "IBM"
DATABASE_URL = "postgresql://{}:{}@{}:5432/{}".format(
    DB_USER, DB_PASS, "postgres", DB_NAME
)
conn = psycopg2.connect(DATABASE_URL)
def_start_date = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime(
    "%Y-%m-%d"
)
def_end_date = datetime.datetime.now().strftime("%Y-%m-%d")


@dataclass
class FinancialData:
    symbol: str
    date: str
    open_price: str
    close_price: str
    volume: str


@dataclass
class StatisticData:
    start_date: str
    end_date: str
    symbol: str
    average_daily_open_price: float
    average_daily_close_price: float
    average_daily_volume: float


@router.get("/financial_data")
def read_financial(
    start_date: str = def_start_date,
    end_date: str = def_end_date,
    symbol: str = DEFAULT_SYMBOL,
    limit: int = 3,
    page: int = 5,
):
    logging.info(start_date, end_date, symbol, limit, page)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM financial_data WHERE symbol = %s LIMIT = %s OFFSET = %s",
            (symbol, limit, page),
        )
        data = cur.fetchall()
        conn.commit()
    return {
        "data": data,
        "pagination": {"count": 20, "page": 2, "limit": limit, "pages": 7},
        "info": {"error": ""},
    }


@router.get("/statistics")
def read_statistics(
    start_date: str = def_start_date,
    end_date: str = def_end_date,
    symbol: str = DEFAULT_SYMBOL,
):
    logging.info(start_date, end_date, symbol)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT * FROM financial_data WHERE symbol = %s AND date >= %s AND date <= %s",
            (symbol, start_date, end_date),
        )
        data = cur.fetchall()
        conn.commit()

    sum_daily_open_price = 0
    sum_daily_close_price = 0
    sum_daily_volume = 0
    record_nums = len(data)
    for record in data:
        sum_daily_open_price += record[2]
        sum_daily_close_price += record[3]
        sum_daily_volume += record[4]
    return {
        "data": StatisticData(
            start_date,
            end_date,
            symbol,
            sum_daily_open_price / record_nums,
            sum_daily_close_price / record_nums,
            sum_daily_volume / record_nums,
        ),
        "info": {"error": ""},
    }
