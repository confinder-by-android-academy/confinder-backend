import os
import pathlib

import aioworkers_aiohttp.app
from jinja2 import Template

from confinder.data.connector import MongoConnector
from confinder.data.models.base import Model


class Application(aioworkers_aiohttp.app.Application):
    def __init__(self, config, *, context, **kwargs):
        super(Application, self).__init__(config, debug=config.debug, context=context, **kwargs)
        Model.connector = MongoConnector(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'),
                                         'confinder')

        self.context.google_api_key = os.getenv('GOOGLE_CLIENT_ID', '')

        self.timezone = os.getenv('TIMEZONE', 'Europe/Moscow')
