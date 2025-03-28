"""Load Candles use case implementation."""

from dataclasses import dataclass, field

from app.core.date_time import Timestamp
from app.core.entities import Security, Timeframe
from app.core.market_data_loader import IMarketDataLoader, MarketDataLoaderRequest
from app.dependency import get_logger
from app.use_cases.base import (
    BaseUseCase,
    UseCaseEvent,
    UseCaseRequest,
    UseCaseResponse,
)

logger = get_logger()


@dataclass
class LoadCandlesEvent(UseCaseEvent):
    """LoadCandles Event."""

    security: Security
    timeframe: Timeframe
    time_from: Timestamp
    time_till: Timestamp


@dataclass
class LoadCandlesRequest(UseCaseRequest):
    """LoadCandles Request."""

    security_ticker: str
    security_board: str
    timeframe: Timeframe
    time_from: Timestamp
    time_till: Timestamp


@dataclass
class LoadCandlesResponse(UseCaseResponse):
    """LoadCandles Response."""

    result: None = None
    errors: list[str] = field(default_factory=list)


class LoadCandles(BaseUseCase):
    """LoadCandles use case."""

    def __init__(
        self,
        market_data_loader: IMarketDataLoader,
    ):
        """Initialize."""
        self.market_data_loader = market_data_loader

    async def execute(self, request: LoadCandlesRequest) -> LoadCandlesResponse:
        """Execute."""
        logger.debug(
            "LoadCandles.execute",
            ticker=request.security_ticker,
            board=request.security_board,
            timeframe=request.timeframe,
            time_from=request.time_from,
            time_till=request.time_till,
        )
        security = Security(
            ticker=request.security_ticker,
            board=request.security_board,
        )
        mdl_request = MarketDataLoaderRequest(
            security=security,
            timeframe=request.timeframe,
            time_from=request.time_from,
            time_till=request.time_till,
        )
        await self.market_data_loader.load_candles(mdl_request)
        response = LoadCandlesResponse()
        event = LoadCandlesEvent(
            security=security,
            timeframe=request.timeframe,
            time_from=request.time_from,
            time_till=request.time_till,
        )
        await self.log_event(event=event)
        return response
