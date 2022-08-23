import dataclasses
import io
import logging
import pathlib
import time
from base64 import b64encode
from typing import Iterator, Optional

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from PIL import Image  # type: ignore
from starlette.responses import StreamingResponse
from starlette.routing import Route

from .adb_helper import AdbHelper
from .camera import AndroidCamera, CameraManager, DummyGamingCamera
from .decode_script import DecodeScript

saved_images_dir = pathlib.Path(__file__).parents[1] / "assets" / "saved_images"

_logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/game/video")
async def video_feed() -> StreamingResponse:
    camera = DummyGamingCamera(size=(100, 200))

    def stream() -> Iterator[bytes]:
        _logger.info("stream started!")
        try:
            for frame in camera.generate():
                yield b"--frame\r\n" b"Content-Type: image/webp\r\n\r\n" + frame.data + b"\r\n"
                time.sleep(0.001)
        except Exception:
            _logger.exception("Exception Occured")
        finally:
            _logger.info("stream has done.")

    return StreamingResponse(stream(), media_type="multipart/x-mixed-replace; boundary=frame")


android_camera = AndroidCamera()
camera_manager = CameraManager(android_camera)
camera_manager.start()


@router.get("/android/video")
async def android_video_feed() -> StreamingResponse:
    def stream() -> Iterator[bytes]:
        _logger.info("stream started!")
        try:
            for frame in android_camera.generate():
                yield b"--frame\r\n" b"Content-Type: image/webp\r\n\r\n" + frame.data + b"\r\n"
                time.sleep(0.001)
        except Exception:
            _logger.exception("Exception Occured")
        finally:
            _logger.info("stream has done.")

    return StreamingResponse(stream(), media_type="multipart/x-mixed-replace; boundary=frame")


@dataclasses.dataclass
class ImageResult:
    base64: str
    uuid: str
    width: int
    height: int


@router.get("/android/image", response_model=ImageResult)
async def android_image() -> ImageResult:
    uuid, frame = camera_manager.webp_frame()
    assert frame is not None
    base64 = b64encode(frame.data).decode("ascii")
    return ImageResult(uuid=uuid, base64=base64, width=frame.width, height=frame.height)


@router.put("/android/image/crop/save")
async def android_save_crop_image(uuid: str, x: int, y: int, width: int, height: int, name: str) -> None:
    frame = camera_manager.from_uuid(uuid)
    assert frame is not None

    with io.BytesIO(frame.data) as f:
        with Image.open(f) as image:
            image.crop((x, y, x + width, y + height)).save(saved_images_dir / f"{name}.png")


@router.post("/android/click")
async def android_click(x: int, y: int) -> None:
    adb = AdbHelper()
    adb.click(x, y)


@router.get("/android/scripts", response_model=list[str])
async def android_scripts() -> list[str]:
    scripts = DecodeScript(AdbHelper())
    return scripts.scripts()


@router.post("/android/scripts/{script}")
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


def stop() -> None:
    camera_manager.stop()
    android_camera.stop()
