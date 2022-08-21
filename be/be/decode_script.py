import pathlib
from tokenize import ENCODING, ENDMARKER, NAME, NEWLINE, NUMBER, OP, TokenInfo, tokenize

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
            if token.type in [ENCODING, ENDMARKER, NEWLINE]:
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
                    elif t.type in [NAME, NUMBER]:
                        args.append(t)

                if token.string == "sleep":
                    self._sleep(args)
                elif token.string == "click":
                    self._click(args)
                elif token.string == "swipe":
                    self._swipe(args)
                else:
                    raise NotImplementedError
            else:
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

    def _swipe(self, args: list[TokenInfo]) -> None:
        assert len(args) == 4
        for i in range(4):
            assert args[i].type == NUMBER
        self._adb.swipe(int(args[0].string), int(args[1].string), int(args[2].string), int(args[3].string))
