from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from motor.motor_asyncio import AsyncIOMotorClient
from redis import Redis
import os

app = FastAPI()

Instrumentator().instrument(app).expose(app)

# Redis 연결
redis = Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    decode_responses=True
)

# MongoDB 연결
mongo_client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://mongo:27017/myapp"))
db = mongo_client.myapp

@app.get("/")
async def root():
    return {
        "message": "Hello World",
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 