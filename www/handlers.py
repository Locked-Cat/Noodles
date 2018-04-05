#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import time

from noodleFramework import get, post
from models import User, Blog


@get('/')
async def index(request):
    blogs = [
        Blog(id='1', title='你好', created_at=time.time() - 120),
        Blog(id='2', title='世界', created_at=time.time() - 3600)
    ]
    return {
        '__template__': 'blogs.html',
        'blogs': blogs
    }