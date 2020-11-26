from sqlalchemy import Column, DateTime, Float, Integer, desc
from sqlalchemy.exc import IntegrityError

from .base import Base, session_scope


class BaseCandleMixin:
    time = Column(DateTime, primary_key=True, nullable=False)
    open = Column(Float)
    close = Column(Float)
    low = Column(Float)
    high = Column(Float)
    volume = Column(Integer)

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
