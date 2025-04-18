from abc import ABC, abstractmethod

from app.core.date_time import Timestamp
from app.core.entities import Candle, Security, Timeframe
from app.core.repository.base import IRepository


class ICandleRepository(IRepository, ABC):

    @abstractmethod
    def __aiter__(self) -> "ICandleRepository":
        raise NotImplementedError

    @abstractmethod
    async def __anext__(self) -> Candle:
        raise NotImplementedError

    @abstractmethod
    def filter_by_security(self, security: Security) -> "ICandleRepository":
        raise NotImplementedError

    @abstractmethod
    def filter_by_timestamp_gte(self, timestamp: Timestamp) -> "ICandleRepository":
        raise NotImplementedError

    @abstractmethod
    def filter_by_timestamp_lte(self, timestamp: Timestamp) -> "ICandleRepository":
        raise NotImplementedError

    @abstractmethod
    def filter_by_timeframe(self, timeframe: Timeframe) -> "ICandleRepository":
        raise NotImplementedError
