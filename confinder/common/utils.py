import logging
import re

import aiohttp

re_class_name = re.compile(r'([A-Z]*[a-z]*)')


async def get(path, params, headers, username=None, password=None):
    auth = None
    if username and password:
        auth = aiohttp.BasicAuth(login=username, password=password)
    async with aiohttp.ClientSession(headers=headers, auth=auth) as session:
        async with session.get(path, params=params) as r:
            result = await r.json()
            logging.info(f'/GET: path {path} status {result}')
            logging.info(headers)
            return result


async def post(path, headers, data):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(path, data=data) as r:
            result = await r.json()
            logging.info(f'/POST: path {path} status {result}')
            logging.info(headers)


async def put(path, headers, data):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.put(path, data=data) as r:
            result = await r.json()
            logging.info(f'/PUT: path {path} status {result}')
            logging.info(headers)


class classproperty(object):  # noqa
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


def convert_class_name(name):
    """
    >>> convert_class_name('ClassName')
    'class_name'
    >>> convert_class_name('ABClassName')
    'abclass_name'
    """
    li = re_class_name.findall(name)
    return '_'.join(i.lower() for i in li if i)


def run_solution(containter_name):
    pass
