from fastapi import FastAPI
from routes.mongo import router as mongo_router
from routes.postgres import router as postgres_router

app = FastAPI()

app.include_router(mongo_router, prefix="/mongo")
app.include_router(postgres_router, prefix="/postgres")
