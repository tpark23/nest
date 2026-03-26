from fastapi import FastAPI

from app.routers import health, statements

app = FastAPI()

app.include_router(health.router)
app.include_router(statements.router)