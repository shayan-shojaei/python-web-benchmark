from bson import ObjectId
from flask import Blueprint, jsonify, request, abort
from sqlalchemy import delete
from database.mongo import collection
from common.models import PostgresItem
from database.postgres import PostgresDatabase

router = Blueprint('postgres', __name__, url_prefix='/postgres')


@router.post('/')
async def create_one() -> PostgresItem:
    body = request.get_json()

    new_item = PostgresItem(**body)

    with PostgresDatabase() as db:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

    return jsonify({
        'id': new_item.id,
        'name': new_item.name,
    })


@router.get('/<id>')
async def find_one(id: str) -> PostgresItem:
    with PostgresDatabase() as db:
        post = db.query(PostgresItem).filter(PostgresItem.id == id).first()

        if post is None:
            return abort(404)

        return jsonify({
            'id': post.id,
            'name': post.name,
        })


@router.put('/<id>')
async def update_one(id: str) -> PostgresItem:
    body = request.get_json()

    with PostgresDatabase() as db:
        item = db.query(PostgresItem).filter(PostgresItem.id == id)

        if item.first() is None:
            return abort(404)

        item.update(body)
        db.commit()

        return jsonify({
            'id': item.first().id,
            'name': item.first().name,
        })


@router.delete('/<id>')
async def delete_one(id: str):
    with PostgresDatabase() as db:
        command = delete(PostgresItem).where(PostgresItem.id == id)
        result = db.execute(command)
        db.commit()

        if result.rowcount == 0:
            return abort(404)

    return jsonify({"success": True})
