#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from noodleFramework import get, post
from models import User

@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'index.html',
        'users': users
    }