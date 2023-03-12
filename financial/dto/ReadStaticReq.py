import datetime
from pydantic import BaseModel, validator
from enum import Enum

DEF_START_DATE = (datetime.datetime.now() - datetime.timedelta(days=14)).strftime(
    "%Y-%m-%d"
)
DEF_END_DATE = datetime.datetime.now().strftime("%Y-%m-%d")


class SymbolEnum(str, Enum):
    IBM = "IBM"
    AAPL = "AAPL"


class ReadStaticReq(BaseModel):
    start_date: datetime.date = DEF_START_DATE
    end_date: datetime.date = DEF_END_DATE
    symbol: SymbolEnum = SymbolEnum.IBM

    @validator("start_date")
    def parse_start_date(cls, value):
        return value.isoformat()

    @validator("end_date")
    def parse_end_date(cls, value):
        return value.isoformat()
