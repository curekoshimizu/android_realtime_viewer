import subprocess
import time


class AdbHelper:
    def __init__(self) -> None:
        pass

    def click(self, x: int, y: int) -> None:
        cmd = ["adb", "shell", "input", "tap", str(x), str(y)]
        subprocess.run(cmd)

    def swipe(self, x: int, y: int, offset_x: int = 0, offset_y: int = 0) -> None:
        cmd = ["adb", "shell", "input", "swipe", str(x), str(y), str(x + offset_x), str(y + offset_y)]
        subprocess.run(cmd)

    def text(self, text: str, ime_installed: bool = True) -> None:
        cmd = ["adb", "shell", "input", "text", text]
        subprocess.run(cmd)

    def sleep(self, ms: int) -> None:
        time.sleep(ms / 1000.0)
