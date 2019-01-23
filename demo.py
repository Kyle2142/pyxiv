#!/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import sys

from pyxiv import *

sys.dont_write_bytecode = True


## change _USERNAME,_PASSWORD first!
_USERNAME = "userbay"
_PASSWORD = "userpay"
_TEST_WRITE = False

## If a special network environment is met, please configure aiohttp as you need.
## Otherwise, just keep it empty.
_AIOHTTP_KWARGS = {
    # 'proxies': {
    #   'https': 'http://127.0.0.1:1087',
    # },
    # 'verify': False,       # PAPI use https, an easy way is disable aiohttp SSL verify
}


## AppAPI start

async def appapi_illust(aapi):
    json_result = await aapi.illust_detail(59580629)
    print(json_result)
    illust = json_result.illust
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    json_result = await aapi.illust_comments(59580629)
    print(json_result)

    json_result = await aapi.ugoira_metadata(51815717)
    print(json_result)
    metadata = json_result.ugoira_metadata
    print(">>> frames=%d %s" % (len(metadata.frames), metadata.zip_urls.medium))


async def appapi_recommend(aapi):
    json_result = await aapi.illust_recommended(bookmark_illust_ids=[59580629])
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.illust_recommended(**next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print("  > %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    json_result = await aapi.illust_related(59580629)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))


# this section does not work right now
    # get next page
# next_qs = aapi.parse_qs(json_result.next_url)
# json_result = await aapi.illust_related(**next_qs)
    # print(json_result)
# illust = json_result.illusts[0]
# print("  > %s, origin url: %s" % (illust.title, illust.image_urls['large']))


async def appapi_users(aapi):
    json_result = await aapi.user_detail(275527)
    print(json_result)
    user = json_result.user
    print("%s(@%s) region=%s" % (user.name, user.account, json_result.profile.region))

    json_result = await aapi.user_illusts(275527)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.user_illusts(**next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print("  > %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    json_result = await aapi.user_bookmarks_illust(2088434)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    json_result = await aapi.user_following(7314824)
    print(json_result)
    user_preview = json_result.user_previews[0]
    print(">>> %s(@%s)" % (user_preview.user.name, user_preview.user.account))

    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.user_following(**next_qs)
    # print(json_result)
    user_preview = json_result.user_previews[0]
    print("  > %s(@%s)" % (user_preview.user.name, user_preview.user.account))

    json_result = await aapi.user_follower(275527)
    print(json_result)

    json_result = await aapi.user_mypixiv(275527)
    print(json_result)


async def appapi_search(aapi):
    first_tag = None
    response = await aapi.trending_tags_illust()
    for trend_tag in response.trend_tags[:10]:
        if not first_tag:
            first_tag = trend_tag.tag
        print("%s -  %s(id=%s)" % (trend_tag.tag, trend_tag.illust.title, trend_tag.illust.id))

    json_result = await aapi.search_illust(first_tag, search_target='partial_match_for_tags')
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.search_illust(**next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))


async def appapi_ranking(aapi):
    json_result = await aapi.illust_ranking('day_male')
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.illust_ranking(**next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # 2016-07-15 日的过去一周排行
    json_result = await aapi.illust_ranking('week', date='2016-07-15')
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))


async def appapi_auth_api(aapi):
    json_result = await aapi.illust_follow(req_auth=True)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    # get next page
    next_qs = aapi.parse_qs(json_result.next_url)
    json_result = await aapi.illust_follow(req_auth=True, **next_qs)
    # print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))

    json_result = await aapi.illust_recommended(req_auth=True)
    print(json_result)
    illust = json_result.illusts[0]
    print(">>> %s, origin url: %s" % (illust.title, illust.image_urls['large']))


## PAPI start

async def migrate_rev2_to_papi(api):
    print(">>> new ranking_all(mode='daily', page=1, per_page=50)")
    # rank_list = api.sapi.ranking("all", 'day', 1)
    rank_list = api.ranking_all('daily', 1, 50)
    print(rank_list)

    # more fields about response: https://github.com/upbit/pixivpy/wiki/sniffer
    ranking = rank_list.response[0]
    for img in ranking.works:
        # print img.work
        print("[%s/%s(id=%s)] %s" % (img.work.user.name, img.work.title, img.work.id, img.work.image_urls.px_480mw))


async def papi_base(api):
    # PAPI.works
    json_result = api.works(46363414)
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

    # PAPI.users
    json_result = api.users(1184799)
    print(json_result)
    user = json_result.response[0]
    print(user.profile.introduction)


async def papi_me(api):
    # PAPI.me_feeds
    json_result = api.me_feeds(show_r18=0)
    print(json_result)
    # work = json_result.response[0].ref_user.works[0]
    # print(work.title)

    # PAPI.me_favorite_works
    json_result = api.me_favorite_works(publicity='private')
    print(json_result)
    illust = json_result.response[0].work
    print("[%s] %s: %s" % (illust.user.name, illust.title, illust.image_urls.px_480mw))

    # PAPI.me_following_works (New -> Follow)
    json_result = api.me_following_works()
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))


# the following was commented out due to unresolved variables
# if _TEST_WRITE:
#     # PAPI.me_favorite_works_add
#     json_result = api.me_favorite_works_add(ref_work.id, publicity='private')
#     print(json_result)
#     favorite_id = json_result.response[0].id
#     print(">>> Add favorite illust_id=%s success! favorite_id=%s" % (ref_work.id, favorite_id))
#
#     # PAPI.me_favorite_works_delete
#     # json_result = api.me_favorite_works_delete([favorite_id, ...], publicity='private')
#     json_result = api.me_favorite_works_delete(favorite_id, publicity='private')
#     print(json_result)


async def papi_me_user(api):
    # PAPI.me_following
    json_result = api.me_following()
    print(json_result)
    user = json_result.response[0]
    print(user.name)

    if _TEST_WRITE:
        # PAPI.me_favorite_users_follow
        user_id = 1184799
        json_result = api.me_favorite_users_follow(user_id)
        print(json_result)
        user = json_result.response[0].target_user
        print(user.name)

        # PAPI.me_favorite_users_unfollow
        json_result = api.me_favorite_users_unfollow(user_id)
        print(json_result)


async def papi_user(api):
    # PAPI.users_works
    json_result = api.users_works(1184799)
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s, origin url: %s" % (illust.caption, illust.image_urls['large']))

    # PAPI.users_favorite_works
    json_result = api.users_favorite_works(1184799)
    print(json_result)
    illust = json_result.response[0].work
    print(">>> %s origin url: %s" % (illust.caption, illust.image_urls['large']))

    # PAPI.users_feeds
    json_result = api.users_feeds(1184799, show_r18=0)
    print(json_result)
    ref_work = json_result.response[0].ref_work
    print(ref_work.title)

    # PAPI.users_following
    json_result = api.users_following(4102577)
    print(json_result)
    user = json_result.response[0]
    print(user.name)


async def papi_ranking(api):
    # PAPI.ranking
    json_result = api.ranking('illust', 'weekly', 1)
    print(json_result)
    illust = json_result.response[0].works[0].work
    print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))

    # PAPI.ranking(2015-05-01)
    json_result = api.ranking(ranking_type='all', mode='daily', page=1, date='2015-05-01')
    print(json_result)
    illust = json_result.response[0].works[0].work
    print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))


async def papi_search(api):
    # PAPI.search_works
    json_result = api.search_works("五航戦 姉妹", page=1, mode='text')
    # json_result = api.search_works("水遊び", page=1, mode='exact_tag')
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s origin url: %s" % (illust.title, illust.image_urls['large']))


async def papi_others(api):
    # PAPI.latest_works (New -> Everyone)
    json_result = api.latest_works()
    print(json_result)
    illust = json_result.response[0]
    print(">>> %s url: %s" % (illust.title, illust.image_urls.px_480mw))


async def old_main():
    # public-api
    api = PixivAPI(**_AIOHTTP_KWARGS)
    await api.login(_USERNAME, _PASSWORD)

    await migrate_rev2_to_papi(api)

    await papi_base(api)
    await papi_me(api)
    await papi_me_user(api)
    await papi_user(api)
    await papi_ranking(api)
    await papi_search(api)
    await papi_others(api)


async def main():
    # app-api
    aapi = AppPixivAPI(**_AIOHTTP_KWARGS)

    await aapi.login(_USERNAME, _PASSWORD)

    await appapi_illust(aapi)
    await appapi_recommend(aapi)
    await appapi_users(aapi)
    await appapi_search(aapi)
    await appapi_ranking(aapi)

    await appapi_auth_api(aapi)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
