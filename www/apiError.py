#!/usr/bin/env python3
#-*- coding: utf-8 -*-

class APIError(Exception):
    def __init__(self, error, data='', message=''):
        super(APIError, self).__init__(message)
        self.error = error
        self.data = data
        self.message = message

class APIValueError(Exception):
    def __init__(self, field, message=''):
        super(APIValueError, self).__init__('value: invalid', field, message)