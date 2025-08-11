import random

import httpx
from fastapi import APIRouter
from pydantic import BaseModel

from app.choice import Choice, decide_winner
from app.settings import settings

router = APIRouter()


@router.get("/choices")
async def get_choices():
    return Choice.choices()


@router.get("/choice")
async def get_choice():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(settings().random_number_url)
            response.raise_for_status()
            num = (response.json()["random_number"] - 1) // 20
            return {"id": num, "name": Choice(num).name}
        except httpx.HTTPStatusError:
            choice = random.choice(Choice.all())
            return {"id": choice.value, "name": choice.name}


class PlayRequest(BaseModel):
    player: Choice = Choice.UNKNOWN


class PlayResponse(BaseModel):
    results: str
    player: Choice
    computer: Choice


@router.post("/play", response_model=PlayResponse)
async def play(request: PlayRequest):
    player_choice = Choice(request.player)
    computer_choice = random.choice(Choice.all())
    result = decide_winner(player_choice, computer_choice)
    return {"results": result, "player": request.player, "computer": computer_choice}
