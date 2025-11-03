from fastapi import FastAPI
from app.routers import events, stats, users

app = FastAPI(title="Event ingestion and Analytics Service")

app.include_router(events.router)
app.include_router(stats.router)
app.include_router(users.router)
