from motor.motor_asyncio import AsyncIOMotorClient as MotorClient

from config import env

client = MotorClient(env.MONGODB_URL)

db = client.TheMafiaHostDB
