import subprocess
import time


class AdbHelper:
    def __init__(self) -> None:
        pass

    def click(self, x: int, y: int) -> None:
        subprocess.run(["adb", "shell" "input", "tap", str(x), str(y)])

    def sleep(self, ms: int) -> None:
        time.sleep(ms / 1000.0)
