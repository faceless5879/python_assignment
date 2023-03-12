import os
from dotenv import load_dotenv
import psycopg2
from fastapi import APIRouter, HTTPException
import datetime

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
print(DATABASE_URL)
connection = psycopg2.connect(DATABASE_URL)
def_start_date = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime(
    "%Y-%m-%d"
)
def_end_date = datetime.datetime.now().strftime("%Y-%m-%d")


@router.get("/financial_data")
async def read_financial(
    start_date: str = def_start_date,
    end_date: str = def_end_date,
    symbol: str = DEFAULT_SYMBOL,
    limit: int = 3,
    page: int = 2,
):
    print(start_date, end_date, symbol, limit, page)

    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/statistics")
async def read_statistics(
    start_date: str = def_start_date,
    end_date: str = def_end_date,
    symbol: str = DEFAULT_SYMBOL,
):
    print(start_date, end_date, symbol)
    return [{"username": "Rick"}, {"username": "Morty"}]
