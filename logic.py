import datetime as dt

import oandapyV20.endpoints.instruments as instruments
import pandas as pd
from oandapyV20.exceptions import V20Error

from db.models import UsdJpyCandle1M
from oanda.AccountManager import AccountManager


class APIClient(AccountManager):
    def __init__(self):
        super().__init__()

    def get_candles(self, granularity, date, instrument):
        """
        指定した1日のcandleを取得する
        """
        params = {
            "granularity": granularity,
            "from": date,
            "to": date + dt.timedelta(days=1),
            "alignmentTimezone": "Asia/Tokyo",
        }
        req = instruments.InstrumentsCandles(instrument, params)
        try:
            return self.client.request(req)
        except V20Error as e:
            print(e)
            return None


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
