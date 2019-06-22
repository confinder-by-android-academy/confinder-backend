import motor.motor_asyncio


class MongoConnector:
    def __init__(self, url, db_name):
        self.url = url
        self.mongo = motor.motor_asyncio.AsyncIOMotorClient(self.url)
        self.db = self.mongo[db_name]

    def __getattr__(self, item):
        return self.db[item]

    def __getitem__(self, key):
        return self.db[key]
