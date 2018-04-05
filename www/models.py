#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import time
import uuid
import logging
import asyncio

from orm import Model, StringField, BooleanField, IntegerField, FloatField, create_connection_pool


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    name = StringField(ddl='varchar(50)')
    email = StringField(ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)


class Blog(Model):
    __table__ = 'blogs'

    id = StringField(primary_key=True, default=next_id, ddl='var char(50)')
    title = StringField(ddl='varchar(50)')
    user_id = StringField(ddl='varchar(50)')
    created_at = FloatField(default=time.time)