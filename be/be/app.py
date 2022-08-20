from dataclasses import dataclass
from typing import Optional
from starlette.routing import Route

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles

router = APIRouter()


@dataclass
class Response:
    resp: str


@router.get("/ping", response_model=list[Response])
async def ping() -> list[Response]:
    return [Response(resp="pong")]


app = FastAPI()


def setup_app(
    use_docs: bool,
    static_dir: Optional[str] = None,
) -> None:
    docs_list = ["/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"]
    if not use_docs:
        routes = []
        for r in app.router.routes:
            if isinstance(r, Route) and r.path in docs_list:
                continue
            routes.append(r)
        routes.append(r)
        app.router.routes = routes
    app.include_router(router, prefix="/api")

    if static_dir is not None:
        app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
