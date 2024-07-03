from bson import ObjectId
from flask import Blueprint, jsonify, request, abort
from database.mongo import collection
from common.models import MongoItem

router = Blueprint('mongo', __name__, url_prefix='/mongo')


@router.post('/')
async def create_one() -> MongoItem:
    body = request.get_json()
    result = await collection.insert_one(MongoItem(name=body['name']).model_dump())
    created_item = await collection.find_one({"_id": result.inserted_id})

    return MongoItem(**created_item).model_dump()


@router.get('/<id>')
async def find_one(id: str) -> MongoItem:
    item = await collection.find_one({"_id": ObjectId(id)})
    if item is None:
        return abort(404)

    return MongoItem(**item).model_dump()


@router.put('/<id>')
async def update_one(id: str) -> MongoItem:
    body = request.get_json()
    result = await collection.find_one_and_update({"_id": ObjectId(id)}, {"$set": body}, return_document=True)

    if result is None:
        return abort(404)

    return MongoItem(**result).model_dump()


@router.delete('/<id>')
async def delete_one(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    success = result.deleted_count == 1

    if not success:
        return abort(404)

    return jsonify({"success": success})
