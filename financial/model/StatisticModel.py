from dataclasses import dataclass


@dataclass
class StatisticModel:
    start_date: str
    end_date: str
    symbol: str
    average_daily_open_price: float
    average_daily_close_price: float
    average_daily_volume: float
