import oandapyV20.endpoints.trades as trades
import settings
from oandapyV20 import API


class AccountManager:
    def __init__(
        self, account_id=settings.account_id, access_token=settings.access_token
    ):
        self.account_id = account_id
        self.access_token = access_token

        self.client = API(access_token=access_token)

    def get_account_info(self):
        r = trades.TradesList(self.account_id)
        rv = self.client.request(r)
        return rv
