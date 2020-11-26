import datetime as dt

import pandas as pd

from db.models import UsdJpyCandle1M
from oanda import APIClient


class Candle(APIClient):
    def __init__(
        self, granularity="M1", date=dt.date(2010, 1, 4), instrument="USD_JPY"
    ):
        super().__init__()
        self.granularity = granularity
        self.date = date
        self.instrument = instrument
        self.__resps = self.get_candles(
            granularity=granularity, date=date, instrument=instrument
        )

    @property
    def values(self):
        if self.__resps is None:
            return None

        candles = []
        for resp in self.__resps["candles"]:
            candle = {
                "time": pd.to_datetime(resp["time"]),
                "volume": resp["volume"],
                "open": resp["mid"]["o"],
                "close": resp["mid"]["c"],
                "high": resp["mid"]["h"],
                "low": resp["mid"]["l"],
            }
            candles.append(candle)
        return candles


if __name__ == "__main__":
    count_date = dt.date(2010, 10, 4)
    for _ in range(7):
        candle = Candle(date=count_date)
        UsdJpyCandle1M.create_by_list(candle.values)

        count_date += dt.timedelta(days=1)
        print(candle)
