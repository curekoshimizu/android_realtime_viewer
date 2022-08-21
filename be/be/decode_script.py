import pathlib

from .adb_helper import AdbHelper

shortcuts_dir = pathlib.Path(__file__).parents[1] / "assets" / "shortcuts"


class DecodeScript:
    def scripts(self) -> list[str]:
        assert shortcuts_dir.exists(), shortcuts_dir
        assert shortcuts_dir.is_dir()
        ret = []
        for p in shortcuts_dir.iterdir():
            if not p.is_file():
                continue
            ret.append(p.stem)
        return ret

    def run(self, script_name: str) -> None:
        pass
