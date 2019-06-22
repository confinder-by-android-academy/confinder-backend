import logging
import os

import aioworkers_redis.base


class Connector(aioworkers_redis.base.Connector):
    def __init__(self, config=None, *, context=None, loop=None):
        redis_host = os.getenv('REDIS_HOST', 'localhost')
        redis_port = os.getenv('REDIS_PORT', 6379)
        if redis_host:
            logging.info(f"Set redis config: {redis_host}")
            config = config.new_child({
                'connection': {
                    'host': redis_host,
                    'port': redis_port,
                }
            })
        super().__init__(config, context=context, loop=loop)
