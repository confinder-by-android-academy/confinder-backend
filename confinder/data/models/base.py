from aioworkers.core.base import AbstractEntity

from confinder.common.utils import classproperty, convert_class_name


class Model(AbstractEntity):
    models = {}
    connector = None
    collection_name = None
    limit = 5000

    def __init_subclass__(cls, **kwargs):
        cls.models[convert_class_name(cls.__name__)] = cls

    def __getattr__(self, item):
        return self.models[item]

    @classproperty
    def collection(self):
        return self.connector[self.collection_name]

    @classproperty
    def c(self):
        return self.connector[self.collection_name]

    @classmethod
    async def get(cls, *args, limit=5000, **kwargs):
        return await cls.collection.find(kwargs).to_list(length=limit)

    @classmethod
    async def get_one(cls, **kwargs):
        return await cls.collection.find_one(kwargs)

    @classmethod
    async def filter(cls, find_filter, **kwargs):
        result = await cls.collection.find(find_filter).to_list(length=cls.limit)
        return result

    @classmethod
    async def delete(cls, **kwargs):
        return await cls.collection.delete_many(kwargs)

    @classmethod
    async def insert_one(cls, item, *args, **kwargs):
        result = await cls.collection.insert_one(item)
        return result

    @classmethod
    async def update_one(cls, update_filter, update, **kwargs):
        result = await cls.collection.update_one(update_filter, update, **kwargs)
        return result
