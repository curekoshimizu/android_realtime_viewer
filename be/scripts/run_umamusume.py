#!/usr/bin/env python

from be.adb_helper import AdbHelper


def go_title_from_lobby(adb: AdbHelper) -> None:
    adb.click(1009, 250)
    adb.sleep(1000)
    adb.swipe(545, 1140, offset_y=-100)
    adb.sleep(1000)
    adb.click(290, 1874)


def delte_account(adb: AdbHelper) -> None:
    adb.click(1013, 2270)
    adb.sleep(500)
    adb.click(541, 1832)
    adb.sleep(500)
    adb.click(791, 1530)
    adb.sleep(500)
    adb.click(791, 1530)
    adb.sleep(500)
    adb.click(543, 1528)


def go_home(adb: AdbHelper) -> None:
    adb.click(780, 1520)
    adb.sleep(500)
    adb.click(300, 1520)
    adb.sleep(500)
    adb.click(780, 1520)
    adb.sleep(500)
    adb.click(300, 1520)


def main() -> None:
    adb = AdbHelper()

    # go_home(adb)
    # adb.sleep(1500)
    # adb.click(500, 1600)
    # adb.sleep(1000)
    # delte_account(adb)
    # adb.sleep(1500)
    # adb.click(500, 1600)
    # adb.sleep(1000)
    adb.click(500, 1600)
    adb.sleep(1000)
    go_title_from_lobby(adb)

    # adb.click(1059, 2159)
    # go_title_from_lobby(adb)


if __name__ in "__main__":
    main()
