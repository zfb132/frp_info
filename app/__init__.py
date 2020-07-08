#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 20-07-08 19:25:56
from flask import Flask
import app.config as config

app = Flask(__name__)
app.secret_key = config.FLASK_SECRET_KEY

from app.controller.main import *

