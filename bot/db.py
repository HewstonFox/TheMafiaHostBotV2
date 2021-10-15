from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
import certifi
from config import env

client = MotorClient(env.MONGODB_URL, tlsCAFile=certifi.where())

db = client.TheMafiaHostDB
