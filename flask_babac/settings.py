#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import yaml


def read_config():

    config_file = Path.home() / ".config" / "flask_babac" / "config.yml"

    if config_file.is_file():

        with config_file.open(mode="r") as file:
            config_info = yaml.safe_load(file)

        username_babac = config_info["Cycle Babac"]["username"]
        password_babac = config_info["Cycle Babac"]["password"]

    else:
        with config_file.open(mode="w") as file:
            yaml.dump(
                {
                    "Cycle Babac": {
                        "username": "BobTheSponge",
                        "password": "BikiniBottom",
                    }
                },
                file,
            )

        username_babac = None
        password_babac = None

    return username_babac, password_babac
