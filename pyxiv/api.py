import asyncio
import hashlib
import json
import os
import shutil
from datetime import datetime

import aiohttp

from .utils import PixivError, JsonDict


class BasePixivAPI(object):
    client_id = 'MOBrBDS8blbauoSck0ZfDbtuzpyT'
    client_secret = 'lsACyCD94FhDUtGTXi3QzcFE2uU1hqtDaKeqrdwj'
    hash_secret = '28c1fdd170a5204386cb1313c7077b34f83e4aaf4aa829ce78c231e05b0bae2c'

    access_token = None
    user_id = 0
    refresh_token = None

    def __init__(self, **aiohttp_kwargs):
        """initialize aiohttp kwargs if need be"""
        self.aiohttp = aiohttp.ClientSession()
        self.aiohttp_kwargs = aiohttp_kwargs
        self.additional_headers = {}

    def __del__(self):
        asyncio.get_event_loop().run_until_complete(self.aiohttp.close())

    def set_additional_headers(self, headers):
        """manually specify additional headers. will overwrite API default headers in case of collision"""
        self.additional_headers = headers

    # 设置HTTP的Accept-Language (用于获取tags的对应语言translated_name)
    # language: en-us, zh-cn, ...
    def set_accept_language(self, language):
        """set header Accept-Language for all requests (useful for get tags.translated_name)"""
        self.additional_headers['Accept-Language'] = language

    @staticmethod
    def parse_json(json_str):
        """parse str into JsonDict"""

        def _obj_hook(pairs):
            """convert json object to python object"""
            o = JsonDict()
            for k, v in pairs.items():
                o[str(k)] = v
            return o

        return json.loads(json_str, object_hook=_obj_hook)

    def require_auth(self):
        if self.access_token is None:
            raise PixivError('Authentication required! Call login() or set_auth() first!')

    async def aiohttp_call(self, method, url, headers=None, params=None, data=None) -> aiohttp.ClientResponse:
        """ aiohttp http/https call for Pixiv API """
        if headers is None:
            headers = {}
        headers.update(self.additional_headers)
        try:
            if method == 'GET':
                return await self.aiohttp.get(url, params=params, headers=headers, **self.aiohttp_kwargs)
            elif method == 'POST':
                return await self.aiohttp.post(url, params=params, data=data, headers=headers, **self.aiohttp_kwargs)
            elif method == 'DELETE':
                return await self.aiohttp.delete(url, params=params, data=data, headers=headers, **self.aiohttp_kwargs)
        except Exception as e:
            raise PixivError('aiohttp %s %s error: %s' % (method, url, e))

        raise PixivError('Unknown method: %s' % method)

    def set_auth(self, access_token, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token

    async def login(self, username, password):
        return await self.auth(username=username, password=password)

    def set_client(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    async def auth(self, username=None, password=None, refresh_token=None):
        """Login with password, or use the refresh_token to acquire a new bearer token"""

        url = 'https://oauth.secure.pixiv.net/auth/token'
        local_time = datetime.now().isoformat()
        headers = {
            'User-Agent': 'PixivAndroidApp/5.0.64 (Android 6.0)',
            'X-Client-Time': local_time,
            'X-Client-Hash': hashlib.md5((local_time+self.hash_secret).encode('utf-8')).hexdigest(),
        }
        data = {
            'get_secure_url': 1,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        if (username is not None) and (password is not None):
            data['grant_type'] = 'password'
            data['username'] = username
            data['password'] = password
        elif (refresh_token is not None) or (self.refresh_token is not None):
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = refresh_token or self.refresh_token
        else:
            raise PixivError('auth() was called but no password or refresh_token was set')

        r = await self.aiohttp_call('POST', url, headers=headers, data=data)
        r.text = await r.text()
        if r.status not in [200, 301, 302]:
            if data['grant_type'] == 'password':
                raise PixivError('auth() failed! check username and password.\nHTTP %s: %s' % (r.status, r.text),
                                 header=r.headers, body=r.text)
            else:
                raise PixivError('auth() failed! check refresh_token.\nHTTP %s: %s' % (r.status, r.text),
                                 header=r.headers, body=r.text)

        token = None
        try:
            # get access_token
            token = self.parse_json(r.text)
            self.access_token = token.response.access_token
            self.user_id = token.response.user.id
            self.refresh_token = token.response.refresh_token
        except:
            raise PixivError('Get access_token error! Response: %s' % token, header=r.headers, body=r.text)

        # return auth/token response
        return token

    async def download(self, url, prefix='', path=os.path.curdir, name=None, replace=False,
                       referer='https://app-api.pixiv.net/'):
        """Download image to file (use 6.0 app-api)"""
        if not name:
            name = prefix + os.path.basename(url)
        else:
            name = prefix + name

        img_path = os.path.join(path, name)
        if (not os.path.exists(img_path)) or replace:
            # Write stream to file
            response = await self.aiohttp_call('GET', url, headers={'Referer': referer})
            with open(img_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
