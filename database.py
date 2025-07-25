import os
import motor.motor_asyncio

CONNECTION_STRING = os.getenv('MONGODB_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)

db = client["artificial_intelligence"]
collection = db["agent_analysis"]


