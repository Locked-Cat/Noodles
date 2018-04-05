#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import functools
import asyncio
import inspect
import logging
import os

from aiohttp import web
from apiError import APIError


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
        
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator


class RequestHandler(object):
    def __init__(self, app, func):
        self._app = app
        self._func = func
        self._has_request_arg = self._test_if_has_request_arg(func)
        self._named_kw_args = self._get_named_kw_args(func)
        self._required_kw_args = self._get_required_kw_args(func)

    def _test_if_has_request_arg(self, func):
        sig = inspect.signature(func)
        params = sig.parameters
        found = False
        for name, param in params.items():
            if name == 'request':
                found = True
                continue
            if found and (param.kind != inspect.Parameter.VAR_POSITIONAL and \
                param.kind != inspect.Parameter.KEYWORD_ONLY and \
                param.kind != inspect.Parameter.VAR_KEYWORD):
                raise ValueError('request parameter must be the last named parameter in function: %s%s' % (func.__name__, str(sig)))
        return found

    def _get_named_kw_args(self, func):
        args = []
        sig = inspect.signature(func)
        params = sig.parameters
        for name, param in params.items():
            if param.kind == inspect.Parameter.KEYWORD_ONLY:
                args.append(name)
        return tuple(args)

    def _get_required_kw_args(self, func):
        args = []
        sig = inspect.signature(func)
        params = sig.parameters
        for name, param in params.items():
            if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
                args.append(name)
        return tuple(args)
           
    async def __call__(self, request):
        kw = None
        if self._named_kw_args:
            if request.method == 'POST':
                if not request.content_type:
                    return web.HTTPBadRequest('Missing Content-Type.')
                content_type = request.content_type
                if content_type.startswith('application/json'):
                    params = await request.json()
                    if not isinstance(params, dict):
                        return web.HTTPBadRequest('JSON body must be object.')
                    kw = params
                elif content_type.startswith('application/x-www-form-urlencoded') or \
                    content_type.startswith('multipart/form-data'):
                    params = await request.post()
                    kw = dict(**params)
                else:
                    return web.HTTPBadRequest('Unsupported Content-Type: %s' % content_type)
        
        if kw is None:
            kw = dict(**request.match_info)
        else:
            if self._named_kw_args:
                copy = dict()
                for arg in self._named_kw_args:
                    if arg in kw:
                        copy[arg] = kw[arg]
                kw = copy

        if self._has_request_arg:
            kw['request'] = request

        for arg in self._required_kw_args:
            if arg not in kw:
                return web.HTTPBadRequest('Missing argument: %s' % arg)

        logging.info('call with args: %s' % str(kw))

        try:
            response = await self._func(**kw)
            return response
        except APIError as e:
            return dict(error=e.error, data=e.data, message=e.message)

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
                add_route(app, func)


def add_static(app):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
    app.router.add_static('/static/', path)
    logging.info('add static %s => %s' % ('/static/', path))