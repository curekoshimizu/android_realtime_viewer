#!/usr/bin/env python

import pathlib

import yaml

from be.app import app, setup_app, stop

root_path = pathlib.Path(__file__).resolve().parents[2]


def main() -> None:
    setup_app(use_docs=False, static_dir=None)
    with open(root_path / "openapi.yaml", "w") as f:
        yaml.dump(app.openapi(), f, sort_keys=False)


if __name__ in "__main__":
    try:
        main()
    finally:
        stop()
