from motor.motor_asyncio import AsyncIOMotorClient
from common.config import MONGO_URI, MONGO_DATABASE

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database(MONGO_DATABASE)

collection = db.get_collection("items")
