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
    adb.click(566, 1792)
    adb.sleep(1900)
    adb.click(559, 1783)
    adb.sleep(3400)
    adb.click(557, 1783)
    adb.sleep(3000)
    adb.click(770, 2071)
    adb.sleep(4100)
    adb.click(718, 2069)
    adb.sleep(5400)
    adb.click(300, 1570)
    adb.sleep(3000)
    adb.click(300, 1570)
    adb.sleep(3700)
    adb.click(672, 1563)
    adb.sleep(3200)
    adb.click(512, 1161)
    adb.sleep(2900)
    adb.click(112, 2087)
    adb.sleep(11600)
    adb.click(927, 1280)
    adb.sleep(3100)
    adb.click(676, 1537)
    adb.sleep(2900)
    adb.click(676, 1535)
    adb.sleep(6600)
    adb.click(985, 2258)
    adb.sleep(200)
    adb.click(985, 2258)
    adb.sleep(2700)
    adb.click(985, 2258)
    adb.sleep(4600)
    adb.click(1002, 2258)
    adb.sleep(4100)
    adb.click(1002, 2258)

    adb.sleep(7100)
    adb.click(1002, 2258)
    adb.sleep(3500)
    adb.click(573, 2040)
    adb.sleep(3400)
    adb.click(529, 1542)
    adb.sleep(3300)
    adb.click(573, 2057)
    adb.sleep(3200)
    adb.click(983, 1795)
    adb.sleep(3300)
    adb.click(644, 2050)
    adb.sleep(2400)
    adb.click(400, 2055)
    adb.sleep(3000)
    adb.click(400, 2055)
    adb.sleep(3000)
    adb.click(400, 2055)
    adb.sleep(3200)
    adb.click(400, 2055)


def main() -> None:
    adb = AdbHelper()

    go_title_from_lobby(adb)
    adb.sleep(1500)
    adb.click(500, 1600)
    adb.sleep(1000)
    delte_account(adb)
    # adb.sleep(4000)
    # go_home(adb)

    # adb.sleep(1500)
    # adb.click(500, 1600)
    # adb.sleep(1000)
    # adb.click(500, 1600)
    # adb.sleep(1000)
    # go_title_from_lobby(adb)

    # adb.click(1059, 2159)
    # go_title_from_lobby(adb)


if __name__ in "__main__":
    main()
