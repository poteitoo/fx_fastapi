import sqlalchemy
from sqlalchemy import Column, DateTime, Float, Integer, desc
from sqlalchemy.exc import IntegrityError

from .base import Base, session_scope


class BaseCandleMixin:
    time = sqlalchemy.Column(sqlalchemy.DateTime, primary_key=True, nullable=False)
    open = sqlalchemy.Column(sqlalchemy.Float)
    close = sqlalchemy.Column(sqlalchemy.Float)
    low = sqlalchemy.Column(sqlalchemy.Float)
    high = sqlalchemy.Column(sqlalchemy.Float)
    volume = sqlalchemy.Column(sqlalchemy.Integer)

    @property
    def values(self):
        return {
            "time": self.time,
            "open": self.open,
            "close": self.close,
            "low": self.low,
            "high": self.high,
            "volume": self.volume,
        }

    @classmethod
    def create(cls, time, open, close, high, low, volume):
        candle = cls(
            time=time, open=open, close=close, high=high, low=low, volume=volume
        )
        try:
            with session_scope() as session:
                session.add(candle)
            return candle
        except IntegrityError:
            return False

    @classmethod
    def create_by_list(cls, candle_lst):
        with session_scope() as session:
            for candle in candle_lst:
                candle = cls(**candle)
                session.add(candle)

    @classmethod
    def get_last_candle(cls):
        with session_scope() as session:
            candle = session.query(cls).order_by(desc(cls.time)).first()
        return candle


class UsdJpyCandle1M(BaseCandleMixin, Base):
    __tablename__ = "USD_JPY_1M"
