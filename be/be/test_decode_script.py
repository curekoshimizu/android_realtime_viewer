from .adb_helper import AdbHelper
from .decode_script import DecodeScript


def test_get_scripts() -> None:
    scripts = DecodeScript(AdbHelper())
    result = scripts.scripts()
    assert "delete_account" in result
    assert "go_title_from_lobby" in result
    assert "test_script" not in result


def test_run() -> None:
    scripts = DecodeScript(AdbHelper())
    scripts.run("test_script")
