import pytest
from httpx import AsyncClient
from app.choice import Choice


@pytest.mark.asyncio
async def test_create_match(client: AsyncClient):
    response = await client.post("/matches/")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_get_match(client: AsyncClient, sample_match):
    match_id = str(sample_match.id)
    response = await client.get(f"/matches/{match_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == match_id
    assert data["completed"] is False


@pytest.mark.asyncio
async def test_get_nonexistent_match(client: AsyncClient):
    fake_uuid = "550e8400-e29b-41d4-a716-446655440000"
    response = await client.get(f"/matches/{fake_uuid}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_play_move(client: AsyncClient, sample_player, sample_match):
    player_id = str(sample_player.id)
    match_id = str(sample_match.id)

    response = await client.post(
        f"/matches/{match_id}", json={"player_id": player_id, "move": Choice.ROCK}
    )
    assert response.status_code == 200
    data = response.json()
    assert not data["completed"]


@pytest.mark.asyncio
async def test_play_move_invalid_match(client: AsyncClient, sample_player):
    player_id = str(sample_player.id)
    fake_match_id = "550e8400-e29b-41d4-a716-446655440000"

    response = await client.post(
        f"/matches/{fake_match_id}", json={"player_id": player_id, "move": Choice.ROCK}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_play_move_invalid_player(client: AsyncClient, sample_match):
    fake_player_id = "550e8400-e29b-41d4-a716-446655440000"
    match_id = str(sample_match.id)

    response = await client.post(
        f"/matches/{match_id}", json={"player_id": fake_player_id, "move": Choice.ROCK}
    )
    assert response.status_code == 404
