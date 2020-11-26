import datetime as dt

import oandapyV20.endpoints.instruments as instruments
from oandapyV20.exceptions import V20Error

from .AccountManager import AccountManager


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
