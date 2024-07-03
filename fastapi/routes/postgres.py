from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import delete
from common.models import PostgresItem, SuccessResult
from sqlalchemy.orm import Session

from common.schema import ItemSchema
from database.postgres import get_db


router = APIRouter(tags=["postgres"])


@router.post('/')
async def create_one(item_schema: ItemSchema, db: Session = Depends(get_db)):

    new_item = PostgresItem(**item_schema.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return new_item


@router.get('/{id}')
async def find_one(id: str, db: Session = Depends(get_db)):
    post = db.query(PostgresItem).filter(PostgresItem.id == id).first()

    if post is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return post


@router.put('/{id}')
async def update_one(id: str, item_schema: ItemSchema, db: Session = Depends(get_db)):
    item = db.query(PostgresItem).filter(PostgresItem.id == id)

    if item.first() is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item.update(item_schema.model_dump())
    db.commit()

    return item.first()


@router.delete('/{id}')
async def delete_one(id: str, db: Session = Depends(get_db)) -> SuccessResult:
    command = delete(PostgresItem).where(PostgresItem.id == id)
    result = db.execute(command)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return SuccessResult(success=True)
