from __future__ import annotations

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
