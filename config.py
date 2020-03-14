#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os


class Config(object):
    SECRET_KEY = os.urandom(24) or "you-will-never-guess"


LANGUAGES = {"en": "English", "fr": "French"}
