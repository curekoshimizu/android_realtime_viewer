import datetime
import pathlib
from tokenize import ENCODING, ENDMARKER, NAME, NEWLINE, NL, NUMBER, OP, STRING, TokenInfo, tokenize

from .adb_helper import AdbHelper

shortcuts_dir = pathlib.Path(__file__).parents[1] / "assets" / "shortcuts"


class DecodeScript:
    def __init__(self, adb: AdbHelper) -> None:
        self._adb = adb

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
