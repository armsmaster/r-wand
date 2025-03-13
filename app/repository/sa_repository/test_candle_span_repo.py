import pytest

from app.repository.sa_repository.test_utils import (
    UOW,
    connection_factory,
    security_repository_factory,
    candle_span_repository_factory,
)
from app.repository.test_candle_span_repo import TestCases


class TestCandleSpanRepoAlchemy:

    @pytest.mark.asyncio
    async def test_create(self):
        cf = connection_factory()
        conn = await anext(aiter(cf))
        await TestCases.execute_create_candle_span(
            UOW(conn),
            security_repository_factory(conn),
            candle_span_repository_factory(conn),
        )

    @pytest.mark.asyncio
    async def test_create_many(self):
        cf = connection_factory()
        conn = await anext(aiter(cf))
        await TestCases.execute_create_many_candle_spans(
            UOW(conn),
            security_repository_factory(conn),
            candle_span_repository_factory(conn),
        )

    @pytest.mark.asyncio
    async def test_slicing(self):
        cf = connection_factory()
        conn = await anext(cf)
        await TestCases.execute_slicing(
            UOW(conn),
            security_repository_factory(conn),
            candle_span_repository_factory(conn),
        )

    @pytest.mark.asyncio
    async def test_filters(self):
        cf = connection_factory()
        conn = await anext(aiter(cf))
        await TestCases.execute_candle_span_filters(
            UOW(conn),
            security_repository_factory(conn),
            candle_span_repository_factory(conn),
        )
