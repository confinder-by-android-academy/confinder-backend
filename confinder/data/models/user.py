from confinder.data.models.base import Model


class User(Model):
    collection_name = 'users'

    @classmethod
    async def create_or_login(cls, user_id, **kwargs):
        return await cls.update_one({
            'user_id': user_id,
        },
            {
                '$set': {
                    'user_id': user_id,
                    **kwargs
                },
            }, upsert=True)
