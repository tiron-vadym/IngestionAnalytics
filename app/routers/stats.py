from datetime import date

from fastapi import Depends, APIRouter, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK

from app.handlers.stats import get_dau, get_top_events, get_retention
from app.dependencies import get_db
from app.schemas.stats import (
    DAURow,
    DAUResponse,
    TopEventRow,
    TopEventResponse,
    RetentionRow,
    RetentionResponse
)

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/dau", response_model=DAUResponse, status_code=HTTP_200_OK)
async def stats_dau(
        from_: date | None = Query(None, alias="from"),
        to: date | None = None,
        segment: str | None = None,
        properties: str | None = Query(None, alias="properties.country"),
        db: AsyncSession = Depends(get_db)
):
    rows = await get_dau(db, from_, to, segment, properties)
    parsed_rows = [
        DAURow(date=r["day"].isoformat(), dau=int(r["dau"]))
        for r in rows
    ]
    return DAUResponse(rows=parsed_rows)


@router.get("/top-events", response_model=TopEventResponse, status_code=HTTP_200_OK)
async def stats_top_events(
        from_: date | None = Query(None, alias="from"),
        to: date | None = None,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    rows = await get_top_events(db, from_, to, limit)
    parsed_rows = [
        TopEventRow(event_type=r["event_type"], count=int(r["cnt"]))
        for r in rows
    ]
    return TopEventResponse(rows=parsed_rows)


@router.get("/retention", response_model=RetentionResponse, status_code=HTTP_200_OK)
async def stats_retention(start_date: date, db: AsyncSession = Depends(get_db)):
    rows = await get_retention(start_date, db)
    parsed_rows = [
        RetentionRow(
            first_day=r["first_day"].isoformat() if r["first_day"] else "",
            days=r["days"] or []
        )
        for r in rows
    ]
    return RetentionResponse(rows=parsed_rows)
