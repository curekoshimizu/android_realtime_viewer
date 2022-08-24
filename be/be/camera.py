from __future__ import annotations

import dataclasses
import io
import subprocess
import threading
import time
from abc import ABC, abstractmethod
from typing import Iterator, Optional, Tuple
from uuid import uuid4

from PIL import Image  # type:ignore


@dataclasses.dataclass
class CapturedResult:
    raw_image: Image.Image
    webp_data: bytes
    height: int
    width: int


class Camera(ABC):
    @abstractmethod
    def generate(self) -> Iterator[CapturedResult]:
        ...


class DummyGamingCamera(Camera):
    def __init__(self, size: Tuple[int, int]) -> None:
        self._size = size

    def color_generator(self) -> Iterator[Tuple[int, int, int]]:
        while True:
            for i in range(256):
                yield (255, i, 0)
            for i in range(256):
                yield (255 - i, 255, 0)
            for i in range(256):
                yield (0, 255, i)
            for i in range(256):
                yield (0, 255 - i, 255)
            for i in range(256):
                yield (i, 0, 255)
            for i in range(256):
                yield (255, 0, 255 - i)

    def generate(self) -> Iterator[CapturedResult]:
        for r, g, b in self.color_generator():
            image = Image.new("RGBA", size=self._size, color=(r, g, b))
            with io.BytesIO() as frame:
                image.save(frame, "webp")
                yield CapturedResult(
                    data=frame.getvalue(),
                    width=image.width,
                    height=image.height,
                )


class AndroidCamera(Camera):
    def __init__(self) -> None:
        self._stop_req = False

    def stop(self) -> None:
        self._stop_req = True

    def screencap2pil(self, width: int, height: int) -> Image.Image:
        pipe = subprocess.Popen("adb shell screencap", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        assert pipe.stdout is not None
        img_bytes = pipe.stdout.read()
        return Image.frombuffer("RGBA", (width, height), img_bytes[12:], "raw", "RGBX", 0, 1)

    def generate(self) -> Iterator[CapturedResult]:
        while not self._stop_req:
            width = 1080
            height = 2340
            try:
                image = self.screencap2pil(width, height)
                with io.BytesIO() as frame:
                    image.save(frame, "webp")
                    yield CapturedResult(
                        raw_image=image,
                        webp_data=frame.getvalue(),
                        width=image.width,
                        height=image.height,
                    )
            except Exception:
                pass
            time.sleep(0.01)


class CameraManager(threading.Thread):
    def __init__(self, camera: Camera) -> None:
        super().__init__()
        self._camera = camera
        self._lock = threading.Lock()
        self._uuid: str = str(uuid4())
        self._frame: Optional[CapturedResult] = None
        self._stop_req = False
        self._db: list[tuple[str, CapturedResult]] = []
        self._threshold_len = 100

    def webp_frame(self) -> tuple[str, Optional[CapturedResult]]:
        with self._lock:
            frame = self._frame
            if frame is not None:
                self._db.append((self._uuid, frame))
                if len(self._db) > self._threshold_len:
                    self._db.pop(0)
            return (self._uuid, self._frame)

    def from_uuid(self, uuid: str) -> Optional[CapturedResult]:
        for db_uuid, ret in self._db:
            if db_uuid == uuid:
                return ret
        return None

    def run(self) -> None:
        for frame in self._camera.generate():
            if self._stop_req:
                return
            with self._lock:
                self._uuid = str(uuid4())
                self._frame = frame

    def stop(self) -> None:
        self._stop_req = True
