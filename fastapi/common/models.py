from typing import Annotated, Optional
from pydantic import BaseModel, BeforeValidator, Field
from sqlalchemy import Column, Integer, String

from database.postgres import Base, engine


PyObjectId = Annotated[str, BeforeValidator(str)]


class MongoItem(BaseModel):
    id: Optional[PyObjectId] = Field(
        alias="_id", default=None, serialization_alias="id")

    name: str


class PostgresItem(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    name = Column(String, nullable=False)


class SuccessResult(BaseModel):
    success: bool


Base.metadata.create_all(bind=engine)
