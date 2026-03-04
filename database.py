# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL=os.getenv("MONGO_URL")


client=AsyncIOMotorClient(MONGO_URL)
database=client.chat_db
messages_collection=database.messages
group_collection=database.broadcastmsge

