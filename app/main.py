from fastapi import FastAPI
from app.api.producer import router as producer_router

app = FastAPI(title="TaskForge")

app.include_router(producer_router)
