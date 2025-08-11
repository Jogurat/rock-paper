import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_player(client: AsyncClient):
    response = await client.post("/players", json={"username": "testuser"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_player_duplicate_username(client: AsyncClient):
    await client.post("/players", json={"username": "testuser"})

    response = await client.post("/players", json={"username": "testuser"})

    assert response.status_code == 400
