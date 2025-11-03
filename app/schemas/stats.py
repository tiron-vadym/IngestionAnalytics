from pydantic import BaseModel


class DAURow(BaseModel):
    date: str
    dau: int


class DAUResponse(BaseModel):
    rows: list[DAURow]


class TopEventRow(BaseModel):
    event_type: str
    count: int


class TopEventResponse(BaseModel):
    rows: list[TopEventRow]


class RetentionRow(BaseModel):
    first_day: str
    days: list[int]


class RetentionResponse(BaseModel):
    rows: list[RetentionRow]
