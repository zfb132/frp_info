#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: 'zfb'
# time: 20-07-08 19:20:22
from app import app
from log import initLog

logging = initLog('frp-info.log','runserver')

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=6665)

application = app
