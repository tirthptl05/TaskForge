from fastapi import FastAPI
from app.api.producer import router as producer_router
from app.api.dlq import router as dlq_router
from app.api.tasks import router as tasks_router
from app.api.metrics_api import router as metrics_router


app = FastAPI(title="TaskForge")

@app.get('/')
def home():
    return {'message':'Welcome to TaskForge'}

app.include_router(producer_router)
app.include_router(dlq_router)
app.include_router(tasks_router)
app.include_router(metrics_router)
