import datetime
import pathlib
import numpy as np
import json
import time
from tokenize import ENCODING, ENDMARKER, NAME, NEWLINE, NL, NUMBER, OP, STRING, TokenInfo, tokenize
from typing import Optional

from PIL import Image  # type: ignore
from PIL import ImageChops

from .adb_helper import AdbHelper
from .camera import CameraManager

shortcuts_dir = pathlib.Path(__file__).parents[1] / "assets" / "shortcuts"
saved_images_dir = pathlib.Path(__file__).parents[1] / "assets" / "saved_images"


class DecodeScript:
    def __init__(self, adb: AdbHelper, camera_manager: Optional[CameraManager] = None) -> None:
        self._adb = adb
        self._camera_manager = camera_manager

    def scripts(self) -> list[str]:
        assert shortcuts_dir.exists(), shortcuts_dir
        assert shortcuts_dir.is_dir()
        ret = []
        for p in shortcuts_dir.iterdir():
            if not p.is_file():
                continue
            name = p.stem
            if "test_" in name:
                continue
            ret.append(p.stem)
        return ret

    def run(self, script_name: str) -> None:
        fname = shortcuts_dir / f"{script_name}.script"
        with open(fname, "rb") as f:
            tokens = list(tokenize(f.readline))

        index = 0
        while index < len(tokens):
            token = tokens[index]
            if token.type in [ENCODING, ENDMARKER, NEWLINE, NL]:
                index += 1
            elif token.type == NAME:
                index += 1
                op = tokens[index]
                assert op.type == OP and op.string == "("

                args = []
                while True:
                    index += 1
                    t = tokens[index]
                    if t.type == OP and t.string == ")":
                        index += 1
                        break
                    elif t.type == OP and t.string == ",":
                        continue
                    elif t.type == OP and t.string == "-":
                        args.append(t)
                    elif t.type == NAME:
                        args.append(t)
                    elif t.type == STRING:
                        args.append(t)
                    elif t.type == NUMBER:
                        args.append(t)
                    else:
                        raise NotImplementedError

                operation_name = token.string
                if operation_name == "sleep":
                    self._sleep(args)
                elif operation_name == "click":
                    self._click(args)
                elif operation_name == "swipe":
                    self._swipe(args)
                elif operation_name == "text":
                    self._text(args)
                elif operation_name == "screenshot":
                    self._screenshot(args)
                elif operation_name == "wait_until_detected":
                    self._wait_until_detected(args)
                elif operation_name == "print":
                    self._print(args)
                else:
                    self._call_script(operation_name, args)
            else:
                import ipdb  # type:ignore

                ipdb.set_trace()
                raise NotImplementedError

    def _sleep(self, args: list[TokenInfo]) -> None:
        assert len(args) == 1
        assert args[0].type == NUMBER
        self._adb.sleep(int(args[0].string))

    def _click(self, args: list[TokenInfo]) -> None:
        assert len(args) == 2
        assert args[0].type == NUMBER
        assert args[1].type == NUMBER
        self._adb.click(int(args[0].string), int(args[1].string))

    def _text(self, args: list[TokenInfo]) -> None:
        assert len(args) == 1
        self._adb.text(args[0].string)

    def _screenshot(self, args: list[TokenInfo]) -> None:
        assert len(args) == 0
        name = datetime.datetime.now().strftime("%Y_%m_%d__%H_%M_%S.png")
        self._adb.screenshot(name)

    def _swipe(self, raw_args: list[TokenInfo]) -> None:
        args = []

        is_negative = False
        for arg in raw_args:
            if arg.type == OP and arg.string == "-":
                is_negative = True
            else:
                assert arg.type == NUMBER
                ret = int(arg.string)
                if is_negative:
                    ret *= -1
                args.append(ret)

                is_negative = False

        assert len(args) == 4
        self._adb.swipe(*args)

    def _call_script(self, script_name: str, args: list[TokenInfo]) -> None:
        assert len(args) == 0
        self.run(script_name)

    def _detected(self, image1: Image.Image, image2: Image.Image, threshold: int = 5) -> bool:
        assert image1.size == image2.size
        x = np.array(image1).astype(np.int16).flatten()
        y = np.array(image2).astype(np.int16).flatten()
        diff = np.absolute(x - y)
        ret = (diff < threshold).sum() == len(x)
        return ret

    def _print(self, args: list[TokenInfo]) -> None:
        assert len(args) == 1
        assert args[0].type == STRING
        print(args[0].string)

    def _wait_until_detected(self, args: list[TokenInfo], maximum_time: int = 10) -> None:
        assert len(args) == 1
        assert args[0].type == STRING

        with open(saved_images_dir / f"{eval(args[0].string)}.json") as f:
            data = json.load(f)

        original_image = saved_images_dir / data["image"]
        with Image.open(original_image) as origin:
            origin = origin.convert("L")
            x = data["x"]
            y = data["y"]
            width = origin.width
            height = origin.height

            stime = time.time()
            while True:
                assert self._camera_manager is not None
                _, frame = self._camera_manager.webp_frame()
                assert frame is not None
                image = frame.raw_image
                image = image.crop((x, y, x + width, y + height))
                image = image.convert(origin.mode)
                if self._detected(image, origin):
                    break
                if time.time() - stime > maximum_time:
                    image.save("debug_screen_image.png")
                    import ipdb; ipdb.set_trace()
                    raise TimeoutError()
                time.sleep(0.01)
