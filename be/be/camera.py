from __future__ import annotations
import time
import subprocess

import io
from abc import ABC, abstractmethod
from typing import Iterator, Tuple

from PIL import Image  # type:ignore


class Camera(ABC):
    @abstractmethod
    def generate(self) -> Iterator[bytes]:
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

    def generate(self) -> Iterator[bytes]:
        for r, g, b in self.color_generator():
            image = Image.new("RGBA", size=self._size, color=(r, g, b))
            with io.BytesIO() as frame:
                image.save(frame, "webp")
                yield frame.getvalue()


class AndroidCamera(Camera):
    def screencap2pil(self, width: int, height: int):
        pipe = subprocess.Popen("adb shell screencap", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        img_bytes = pipe.stdout.read()
        return Image.frombuffer("RGBA", (width, height), img_bytes[12:], "raw", "RGBX", 0, 1)

    def generate(self) -> Iterator[bytes]:
        while True:
            width = 1080
            height = 2340
            image = self.screencap2pil(width, height)
            with io.BytesIO() as frame:
                image.save(frame, "webp")
                yield frame.getvalue()
                time.sleep(0.05)
