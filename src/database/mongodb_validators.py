from bson.objectid import ObjectId
from fastapi import HTTPException
import logging

def validate_object_id(id: str):
    try:
    	_id = ObjectId(id)
    except Exception:
    	logging.warning("Invalid Object ID")
    	raise HTTPException(status_code=400, detail="Invalid Object ID")
    return _id