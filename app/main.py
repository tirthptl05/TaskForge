from fastapi import FastAPI
from app.api.producer import router as producer_router

app = FastAPI(title="TaskForge")

@app.get('/')
def home():
    return {'message':'Welcome to TaskForge'}

app.include_router(producer_router)
