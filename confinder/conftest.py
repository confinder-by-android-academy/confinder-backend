import json
import logging
import os
from pathlib import Path

import aioworkers_aiohttp
import pytest
from aiohttp import hdrs
from aioworkers.core.config import Config
from aioworkers.core.context import Context, GroupResolver


@pytest.fixture
def config():

    db_uri = os.getenv('DATABASE_URL')
    if db_uri:
        uri, db_name = db_uri.rsplit('/', maxsplit=1)
        # overcoming difficulties
        if not db_name.startswith('test_'):
            os.environ['DATABASE_URL'] = uri + '/' + 'test_' + db_name

    plugin_config = Path(aioworkers_aiohttp.__file__).with_name('plugin.ini')
    import confinder
    config = Config().load(plugin_config, *confinder.configs)

    # config.checker.autorun = False
    return config


@pytest.fixture
def context(loop, config):
    with Context(
        config, loop=loop,
        # Run all groups
        group_resolver=GroupResolver(include=['web', 'workers', 'engine'])
    ) as ctx:
        yield ctx


@pytest.fixture
def app(context):
    return context.app


@pytest.fixture(scope='session')
def logger():
    return logging.getLogger('test')


@pytest.fixture
def test_server(app):
    from aiohttp.test_utils import TestServer
    return TestServer(app)


@pytest.fixture
def anonym_client(app, test_client, test_server):
    client = app.loop.run_until_complete(test_client(test_server))
    return client


@pytest.fixture
def client_class(context):
    from aiohttp import test_utils

    class TestClient(test_utils.TestClient):
        base_path = '/v1'

        def dumps(self, data):
            return json.dumps(data)

        def request(
                self, method, path, *args,
                parts=None, json=None,
                **kwargs):
            # support name as url
            if isinstance(path, str):
                if not path.startswith('/'):
                    parts = parts or {}
                    path = self.server.app.router[path].url_for(**parts)
                elif self.base_path and not path.startswith(self.base_path):
                    path = self.base_path + path
            # support raw data
            if json is not None:
                kwargs['data'] = self.dumps(json)
                hs = kwargs.setdefault('headers', {})
                hs[hdrs.CONTENT_TYPE] = 'application/json'
            return super().request(
                method=method, path=path, *args, **kwargs)

    return TestClient
