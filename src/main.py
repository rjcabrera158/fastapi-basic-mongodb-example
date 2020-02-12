from fastapi import Depends, FastAPI, Header, HTTPException
from database.mongodb_utils import close_mongo_connection, connect_to_mongo
from pets.routes import pets_router






app = FastAPI(    
		title="Pets API",
    	description="Pets API Documentation",
    	version="1.0.0",)


app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)


app.include_router(
    pets_router,
    prefix="/pets",
    tags=["pets"],
    responses={404: {"description": "Not found"}},
)