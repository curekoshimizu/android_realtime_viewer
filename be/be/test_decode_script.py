from .decode_script import DecodeScript


def test_get_scripts() -> None:
    scripts = DecodeScript()
    result = scripts.scripts()
    assert "delete_account" in result
    assert "go_title_from_lobby" in result
