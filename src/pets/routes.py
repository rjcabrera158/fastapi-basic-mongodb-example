from fastapi import APIRouter, Depends, HTTPException
from typing import List
from starlette.status import HTTP_201_CREATED
from database.mongodb import db
from database.mongodb_validators import validate_object_id

from .model import PetBase, PetKind, PetOnDB, PetBaseUpdateRequest

pets_router = APIRouter()


###############################################################
def fix_pet_id(pet):
    if pet.get("_id", False):
        # change ObjectID to string
        pet["_id"] = str(pet["_id"])
        return pet
    else:
        raise ValueError(
            f"No `_id` found! Unable to fix pet ID for pet: {pet}"
        )

# Get Pet Function.
async def _get_pet_or_404(id: str):
    _id = validate_object_id(id)
    pet = await db.petDB.find_one({"_id": _id})
    if pet:
        return fix_pet_id(pet)
    else:
        raise HTTPException(status_code=404, detail="Pet not found")


#################### ROUTES ###############################
   

@pets_router.post("/addPet", status_code=HTTP_201_CREATED)
async def add_pet(pet: PetBase):
    pet = pet.dict()

    # convert datetime object to string
    pet['petBirthDate'] = pet['petBirthDate'].strftime("%d-%b-%Y") 
    pet_op = await db.petDB.insert_one(pet)
    if pet_op.inserted_id:
        pet = await _get_pet_or_404(pet_op.inserted_id)
        return pet    	


@pets_router.get("/getPet")
async def get_pet(id: str) -> PetBase:
    pet = await _get_pet_or_404(id)
    return pet    


@pets_router.get("/getAllPets", response_model=List[PetOnDB])
async def get_all_pets(petKind: PetKind = None, limit: int = 10, skip: int = 0):
    if petKind is None:
        pets_cursor = db.petDB.find().skip(skip).limit(limit)
    else:
        pets_cursor = db.petDB.find({"petKind": petKind.value}).skip(skip).limit(limit)
    pets = await pets_cursor.to_list(length=limit)
    return list(map(fix_pet_id, pets))


@pets_router.delete("/deletePet",response_model=dict)
async def delete_pet_by_id(id: str):
    await _get_pet_or_404(id)
    pet_op = await db.petDB.delete_one({"_id": validate_object_id(id)})
    if pet_op.deleted_count:
        return {"status": f"deleted count: {pet_op.deleted_count}"}


@pets_router.put("/updatePet",dependencies=[Depends(_get_pet_or_404)])
async def update_pet(id: str, petData: PetBaseUpdateRequest):
    petData = petData.dict()
    petData = {k:v for k,v in petData.items() if v is not None}
    if 'petBirthDate' in petData:
        petData['petBirthDate'] = petData['petBirthDate'].strftime("%d-%b-%Y") 
    pet_op = await db.petDB.update_one(
        {"_id": validate_object_id(id)}, {"$set": petData}
    )
    if pet_op.modified_count:
        return await _get_pet_or_404(id)
    else:
        raise HTTPException(status_code=304)