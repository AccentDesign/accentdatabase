# isort: off
from os import environ

environ.setdefault(
    "DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5433/db"
)

from typing import List

import uvicorn
from accentdatabase import engine, get_session, Base
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import Item

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class ItemIn(BaseModel):
    name: str


class ItemOut(ItemIn):
    id: int

    class Config:
        orm_mode = True


@app.get("/items", response_model=List[ItemOut])
async def items(
    session: AsyncSession = Depends(get_session),
):
    qs = select(Item)
    return (await session.execute(qs)).scalars().all()


@app.post("/items", response_model=ItemOut)
async def add_item(item: ItemIn, session: AsyncSession = Depends(get_session)):
    instance = Item(**item.dict())
    session.add(instance)
    await session.commit()
    return instance


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=80, reload=True)
