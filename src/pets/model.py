from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime,date

class PetKind(str, Enum):
    dog  = "Dog"
    cat  = "Cat"	
    bird = "Bird"

class PetBase(BaseModel):
	petName: str
	petAge: int
	petBreed: str
	petColor: List[str]
	petBirthDate: date
	petKind: PetKind

class PetBaseUpdateRequest(BaseModel):
	petName: str = None
	petAge: int = None
	petBreed: str = None
	petColor: List[str] = None
	petBirthDate: date = None
	petKind: PetKind = None

class PetOnDB(PetBase):
    _id: str
    petBirthDate: str