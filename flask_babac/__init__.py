#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from flask_babac import routes
