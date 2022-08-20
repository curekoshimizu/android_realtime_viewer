from dataclasses import dataclass

from fastapi import APIRouter

router = APIRouter()


@dataclass
class Response:
    resp: str


@router.get("/ping", response_model=list[Response])
async def ping() -> list[Response]:
    return [Response(resp="pong")]
