import os
from dotenv import load_dotenv
import psycopg2
from fastapi import APIRouter, Depends
import logging
from ..dto.ReadFinancialReq import ReadFinancialReq
from ..dto.ReadStaticReq import ReadStaticReq
from ..model.FinancialModel import FinancialModel, Pagination
from ..model.StatisticModel import StatisticModel
import math

router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)
load_dotenv()
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DATABASE_URL = "postgresql://{}:{}@{}:5432/{}".format(
    DB_USER, DB_PASS, "postgres", DB_NAME
)
conn = psycopg2.connect(DATABASE_URL)


@router.get("/financial_data")
def read_financial(req: ReadFinancialReq = Depends()):
    logging.info(req.start_date, req.end_date, req.symbol, req.limit, req.page)
    with conn.cursor() as cur:
        sql = """
        WITH list_financial AS (
            SELECT *
            FROM financial_data
            WHERE symbol = '{}'
                AND "date" <= '{}'
                AND "date" >= '{}'
            ORDER BY "date"
        )
        SELECT (
                SELECT count(*)
                FROM list_financial
            ),
            *
        FROM list_financial
        LIMIT {} OFFSET {}
        """.format(
            req.symbol, req.end_date, req.start_date, req.limit, req.page * req.limit
        )
        cur.execute(sql)
        rows = cur.fetchall()

        products = []
        for row in rows:
            count = row[0]
            symbol = row[1]
            date = row[2]
            open_price = str(row[3])
            close_price = str(row[4])
            volume = str(row[5])
            product = FinancialModel(symbol, date, open_price, close_price, volume)
            products.append(product)

    return {
        "data": products,
        "pagination": Pagination(
            count,
            req.page,
            req.limit,
            math.ceil(count / req.limit),
        ),
    }


@router.get("/statistics")
def read_statistics(req: ReadStaticReq = Depends()):
    logging.info(req.start_date, req.end_date, req.symbol)
    with conn.cursor() as cur:
        sql = "SELECT * FROM financial_data WHERE symbol = '{}' AND date >= '{}' AND date <= '{}'".format(
            req.symbol, req.start_date, req.end_date
        )
        cur.execute(sql)
        data = cur.fetchall()

    record_nums = len(data)
    if record_nums < 1:
        return {"info": "There is no data matched with input parameters"}

    sum_daily_open_price = 0
    sum_daily_close_price = 0
    sum_daily_volume = 0
    for record in data:
        sum_daily_open_price += record[2]
        sum_daily_close_price += record[3]
        sum_daily_volume += record[4]
    return {
        "data": StatisticModel(
            req.start_date,
            req.end_date,
            req.symbol,
            sum_daily_open_price / record_nums,
            sum_daily_close_price / record_nums,
            sum_daily_volume / record_nums,
        )
    }
