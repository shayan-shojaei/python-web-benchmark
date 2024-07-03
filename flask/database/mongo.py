from motor.motor_asyncio import AsyncIOMotorClient
from common.config import MONGO_URI, MONGO_DATABASE
from asyncio import get_event_loop


client = AsyncIOMotorClient(MONGO_URI)

client.get_io_loop = get_event_loop

db = client.get_database(MONGO_DATABASE)

collection = db.get_collection("items")
