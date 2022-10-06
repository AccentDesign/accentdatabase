import pytest
from db import Item


@pytest.mark.asyncio
async def test_is_shared_session(db_session, client):
    instance = Item(name="steve")
    db_session.add(instance)
    await db_session.commit()

    url = "/items"
    response = await client.get(url)
    assert response.status_code == 200
    assert response.json() == [{"id": instance.id, "name": "steve"}]


@pytest.mark.asyncio
async def test_add(client):
    url = "/items"
    data = {"name": "name"}
    response = await client.post(url, json=data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_session_is_rolled_back(client):
    url = "/items"
    data = {"name": "name"}
    response = await client.post(url, json=data)
    assert response.status_code == 200
