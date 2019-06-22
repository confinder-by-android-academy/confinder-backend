import functools
from contextlib import suppress

import aiohttp
import aiohttp.web_exceptions
from aiohttp import web
from google.oauth2 import id_token
from google.auth.transport import requests


def google_auth_permission(arg):
    """
    Use decorator to resolve token to company and check authorization
    """

    def with_arg(view):
        @functools.wraps(view)
        async def wrapper(*args, **kwargs):
            request = kwargs['request']
            token = request.headers.get("API-KEY", '')
            with suppress(ValueError, TypeError):
                request.api_key = token

                idinfo = id_token.verify_oauth2_token(token, requests.Request(), request.app.context.google_api_key)
                if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                    raise ValueError('Wrong issuer.')

                await request.app.context.models.user.create_or_login(user_id=idinfo['sub'], **idinfo)

                request.idinfo = idinfo

                try:
                    r = await view(*args, **kwargs)
                except Exception as e:
                    raise aiohttp.web_exceptions.HTTPServerError()
                return r
            raise aiohttp.web_exceptions.HTTPUnauthorized()

        return wrapper

    if not callable(arg):
        return with_arg
    return with_arg(arg)
