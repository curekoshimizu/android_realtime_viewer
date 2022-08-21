import subprocess
import time
import pathlib

from PIL import Image  # type:ignore

images_dir = pathlib.Path(__file__).parents[1] / "assets" / "images"


class AdbHelper:
    def __init__(self) -> None:
        pass

    def click(self, x: int, y: int) -> None:
        cmd = ["adb", "shell", "input", "tap", str(x), str(y)]
        subprocess.run(cmd)

    def swipe(self, x: int, y: int, offset_x: int, offset_y: int) -> None:
        cmd = ["adb", "shell", "input", "swipe", str(x), str(y), str(x + offset_x), str(y + offset_y)]
        subprocess.run(cmd)

    def text(self, text: str, ime_installed: bool = True) -> None:
        cmd = ["adb", "shell", "input", "text", text]
        subprocess.run(cmd)

    def sleep(self, ms: int) -> None:
        time.sleep(ms / 1000.0)

    def screenshot(self, name: str) -> None:
        width = 1080
        height = 2340

        pipe = subprocess.Popen("adb shell screencap", stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        assert pipe.stdout is not None
        img_bytes = pipe.stdout.read()
        img = Image.frombuffer("RGBA", (width, height), img_bytes[12:], "raw", "RGBX", 0, 1)
        img.convert("RGBA").save(images_dir / name)
