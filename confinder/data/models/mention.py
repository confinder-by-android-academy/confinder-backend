from confinder.data.models.base import Model


class Mention(Model):
    collection_name = 'mentions'

    @classmethod
    async def get_match(cls, user_id):

        my_likes = set(like['mention_id'] for like in await cls.filter(dict(user_id=user_id, mention='like')))
        liked_me = set(like['user_id'] for like in await cls.filter(dict(mention_id=user_id, mention='like')))

        return list(my_likes & liked_me)
