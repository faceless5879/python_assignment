from dataclasses import dataclass


@dataclass
class FinancialModel:
    symbol: str
    date: str
    open_price: str
    close_price: str
    volume: str


@dataclass
class Pagination:
    count: int
    page: int
    limit: int
    pages: int
