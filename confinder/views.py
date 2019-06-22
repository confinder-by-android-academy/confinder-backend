from confinder.permissions import google_auth_permission
from aiohttp import web


@google_auth_permission
async def success(request):
    return dict(status='ok')


@google_auth_permission
async def me(request):
    user = await request.app.context.models.user.get_one(user_id=request.idinfo['sub'])

    return dict(
        id=request.idinfo['sub'],
        given_name=request.idinfo['given_name'],
        family_name=request.idinfo['family_name'],
        picture=request.idinfo['picture'],
        description=user.get('description', ''),
        contacts=user.get('contacts', []),
        tags=user.get('tags', []),
    )


@google_auth_permission
async def change_profile(request, profile):
    await request.app.context.models.user.create_or_login(user_id=request.idinfo['sub'], **profile)
    user = await request.app.context.models.user.get_one(user_id=request.idinfo['sub'])

    return dict(
        id=request.idinfo['sub'],
        given_name=request.idinfo['given_name'],
        family_name=request.idinfo['family_name'],
        picture=request.idinfo['picture'],
        description=user.get('description', ''),
        contacts=user.get('contacts', []),
        tags=user.get('tags', []),
    )


@google_auth_permission
async def conferences(request):
    return [
        dict(
            id=1,
            name='DataArt hackaton',
            description='Pizzaless hackaton',
            picture='https://images.pexels.com/photos/104827/cat-pet-animal-domestic-104827.jpeg?cs=srgb&dl=animal-animal-photography-cat-104827.jpg&fm=jpg',
        )
    ]


@google_auth_permission
async def swipe_list(request, conference_id):
    liked_or_disliked = [like['mention_id'] for like in await request.app.context.models.mention.filter(dict(user_id=request.idinfo['sub']))]

    users = await request.app.context.models.user.filter({
        'user_id': {
            '$nin': liked_or_disliked + [str(request.idinfo['sub'])],
        }
    })

    serialized_users = [
        dict(
            id=user['user_id'],
            given_name=user['given_name'],
            family_name=user['family_name'],
            picture=user['picture'],
            description=user['description'],
            contacts=user['contacts'],
            tags=user['tags'],
        ) for user in users
    ]

    # TODO: serialize info from db

    return serialized_users


@google_auth_permission
async def matches(request):
    user_ids = await request.app.context.models.mention.get_match(
        request.idinfo['sub']
    )

    users = await request.app.context.models.user.filter({
        'user_id': {
            '$in': user_ids,
        }
    })

    serialized_users = [
        dict(
            id=user['user_id'],
            given_name=user['given_name'],
            family_name=user['family_name'],
            picture=user['picture'],
            description=user['description'],
            contacts=user['contacts'],
            tags=user['tags'],
        ) for user in users
    ]
    # TODO: serialize info from db

    return serialized_users


@google_auth_permission
async def like(request, user_id):
    await request.app.context.models.mention.insert_one(dict(
        user_id=request.idinfo['sub'],
        mention_id=user_id,
        mention='like',
    ))

    return dict(
        match=False,
    )


@google_auth_permission
async def dislike(request, user_id):
    await request.app.context.models.mention.insert_one(dict(
        user_id=request.idinfo['sub'],
        mention_id=user_id,
        mention='dislike',
    ))

    return dict(
        status='ok'
    )


@google_auth_permission
async def participate(request, conference_id):

    is_already_participate = await request.app.context.models.participate.get_one(
        user_id=request.idinfo['sub'],
        conference_id=conference_id,
    )

    if not is_already_participate:
        await request.app.context.models.participate.insert_one(dict(
            user_id=request.idinfo['sub'],
            conference_id=conference_id,
        ))
        return dict(status='ok')
    else:
        return web.Response(body='fuck you', content_type='text/html', status=403)
