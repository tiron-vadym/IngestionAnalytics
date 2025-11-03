from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette.status import HTTP_202_ACCEPTED, HTTP_429_TOO_MANY_REQUESTS

from app.dependencies import verify_jwt
from app.schemas.events import EventRequest
from app.utils import rate_limiter
from app.workers.events_worker import enqueue_events

router = APIRouter(tags=["events"])


@router.post("/events", status_code=HTTP_202_ACCEPTED)
async def post_events_async(
        events: list[EventRequest],
        request: Request,
        user: HTTPAuthorizationCredentials = Depends(verify_jwt)
):
    client = request.client.host if request.client else "anon"
    if not rate_limiter.allow(client):
        raise HTTPException(
            status_code=HTTP_429_TOO_MANY_REQUESTS,
            detail="rate limit exceeded"
        )

    batch_dicts = [e.model_dump() for e in events]
    await enqueue_events(batch_dicts)

    return Response(status_code=HTTP_202_ACCEPTED)
