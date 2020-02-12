import logging

from motor.motor_asyncio import AsyncIOMotorClient
from .mongodb import db

async def connect_to_mongo():
    logging.info("connecting to mongo...")
    db.client = AsyncIOMotorClient(str("localhost:27017"),
                                   maxPoolSize=10,
                                   minPoolSize=10)
    # get a collection 
    # Format db.<database_name>.<collection_name>
    db.petDB = db.client.tancho_ci_db.pet
    logging.info("connected to tancho_ci_db/pet")


async def close_mongo_connection():
    logging.info("closing connection...")
    db.client.close()
    logging.info("closed connection")