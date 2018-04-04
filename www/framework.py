#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import functools
import asyncio
import inspect
import logging


def get(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator


def post(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator


class RequestHandler(object):
    def __init__(self, app, func):
        self._app = app
        self._func = func

    async def __call__(self, request):
        pass


def add_route(app, func):
    method = getattr(func, '__method__', None)
    route = getattr(func, '__route__', None)

    if method is None or route is None:
        raise ValueError('@get or @post not defined in %s.' % func.__name__)
    
    if not asyncio.iscoroutinefunction(func) and not inspect.isgeneratorfunction(func):
        func = asyncio.coroutine(func)

    logging.info('add route %s %s => %s' % (method, route, func.__name__))
    app.router.add_route(method, route, RequestHandler(app, func))


def add_routes(app, moudle_name):
    n = moudle_name.rfind('.')
    if n == -1:
        mod = __import__(moudle_name, globals(), locals())
    else:
        name = moudle_name[n + 1:]
        mod = getattr(__import__(moudle_name[:n], globals(), locals(), [name]), name)

    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        func = getattr(mod, attr)
        if callable(func):
            method = getattr(func, '__method__', None)
            route = getattr(func, '__route__', None)
            if method and route:
                add_route(app, method)