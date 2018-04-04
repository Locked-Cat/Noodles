#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import logging
import os
import json
import time
import asyncio

from aiohttp import web
from datetime import datetime


def index(request):
    return web.Response(body=b'<h1>Noodles</h1>', headers={'content-type':'text/html'})


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at htpp://127.0.0.1:9000...')
    return srv


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()