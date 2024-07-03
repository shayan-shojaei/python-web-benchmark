from bson import ObjectId
from fastapi import HTTPException
from fastapi.routing import APIRouter
from common.schema import ItemSchema
from database.mongo import collection
from common.models import MongoItem, SuccessResult

router = APIRouter(tags=["mongo"])


@router.post('/')
async def create_one(item: ItemSchema) -> MongoItem:
    result = await collection.insert_one(item.model_dump())
    created_item = await collection.find_one({"_id": result.inserted_id})
    return created_item


@router.get('/{id}')
async def find_one(id: str) -> MongoItem:
    item = await collection.find_one({"_id": ObjectId(id)})

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.put('/{id}')
async def update_one(id: str, item: ItemSchema) -> MongoItem:
    result = await collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": item.model_dump()}, return_document=True)

    if result is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return result


@router.delete('/{id}')
async def delete_one(id: str) -> SuccessResult:
    result = await collection.delete_one({"_id": ObjectId(id)})
    success = result.deleted_count == 1
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return SuccessResult(success=success)
