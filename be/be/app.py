import logging
import time
from typing import Iterator, Optional

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import StreamingResponse
from starlette.routing import Route

from .adb_helper import AdbHelper
from .camera import AndroidCamera, DummyGamingCamera
from .decode_script import DecodeScript

_logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/game/video")
async def video_feed() -> StreamingResponse:
    camera = DummyGamingCamera(size=(100, 200))

    def stream() -> Iterator[bytes]:
        _logger.info("stream started!")
        try:
            for frame in camera.generate():
                yield b"--frame\r\n" b"Content-Type: image/webp\r\n\r\n" + frame + b"\r\n"
                time.sleep(0.001)
        except Exception:
            _logger.exception("Exception Occured")
        finally:
            _logger.info("stream has done.")

    return StreamingResponse(stream(), media_type="multipart/x-mixed-replace; boundary=frame")


@router.get("/android/video")
async def android_video_feed() -> StreamingResponse:
    camera = AndroidCamera()

    def stream() -> Iterator[bytes]:
        _logger.info("stream started!")
        try:
            for frame in camera.generate():
                yield b"--frame\r\n" b"Content-Type: image/webp\r\n\r\n" + frame + b"\r\n"
                time.sleep(0.001)
        except Exception:
            _logger.exception("Exception Occured")
        finally:
            _logger.info("stream has done.")

    return StreamingResponse(stream(), media_type="multipart/x-mixed-replace; boundary=frame")


@router.post("/android/click")
async def android_click(x: int, y: int) -> None:
    adb = AdbHelper()
    adb.click(x, y)


@router.get("/android/scripts", response_model=list[str])
async def android_scripts() -> list[str]:
    scripts = DecodeScript(AdbHelper())
    return scripts.scripts()


@router.post("/android/scripts/:script")
async def android_run_script(script: str) -> None:
    scripts = DecodeScript(AdbHelper())
    scripts.run(script)


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
