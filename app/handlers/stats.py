from datetime import date

from sqlalchemy import func, distinct, cast, Date, case, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.events import Event


async def get_dau(
    session: AsyncSession,
    date_from: date | None = None,
    date_to: date | None = None,
    segment: str | None = None,
    properties: str | None = None
):
    filters = []
    group_cond = None
    having_cond = None

    if date_from:
        filters.append(Event.occurred_at >= date_from)
    if date_to:
        filters.append(Event.occurred_at <= date_to)

    if segment:
        field_name, value = segment.split(":", 1)

        if field_name == "event_type":
            group_cond = Event.event_type
            having_cond = Event.event_type == value

    if properties:
        filters.append(Event.properties["country"].astext == properties)

    day_trunc = func.date_trunc("day", Event.occurred_at).label("day")

    stmt = select(
        day_trunc,
        func.count(distinct(Event.user_id)).label("dau")
    )

    if group_cond is not None:
        stmt = stmt.add_columns(group_cond.label("segment"))

    if filters:
        stmt = stmt.where(and_(*filters))

    group_by_fields = [day_trunc]
    if group_cond is not None:
        group_by_fields.append(group_cond)

    stmt = stmt.group_by(*group_by_fields)

    if having_cond is not None:
        stmt = stmt.having(having_cond)

    stmt = stmt.order_by(day_trunc)

    result = await session.execute(stmt)
    return result.mappings().all()


async def get_top_events(
        session: AsyncSession,
        date_from: date | None = None,
        date_to: date | None = None,
        limit: int = 10
):
    stmt = (
        select(
            Event.event_type,
            func.count().label('cnt')
        )
        .group_by(Event.event_type)
        .order_by(func.count().desc())
        .limit(limit)
    )

    if date_from and date_to:
        stmt = stmt.where(Event.occurred_at.between(date_from, date_to))

    result = await session.execute(stmt)
    return result.mappings().all()


async def get_retention(start_date: date, session: AsyncSession):
    first_day_cte = (
        select(
            Event.user_id,
            cast(func.date_trunc('day', func.min(Event.occurred_at)), Date).label('first_day')
        )
        .where(Event.occurred_at >= start_date)
        .group_by(Event.user_id)
        .cte('first_day')
    )

    events_by_day_cte = (
        select(
            Event.user_id,
            cast(func.date_trunc('day', Event.occurred_at), Date).label('day')
        )
        .where(Event.occurred_at >= start_date)
        .cte('events_by_day')
    )

    stmt = (
        select(
            first_day_cte.c.first_day,
            func.array_agg(
                case(
                    (events_by_day_cte.c.day == first_day_cte.c.first_day, 1),
                    else_=0
                )
            ).label('days')
        )
        .outerjoin(
            events_by_day_cte,
            events_by_day_cte.c.user_id == first_day_cte.c.user_id
        )
        .group_by(first_day_cte.c.first_day)
        .limit(100)
    )

    result = await session.execute(stmt)
    return result.mappings().all()
