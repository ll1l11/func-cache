# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from utils import function_namespace, unpack_params_to_dict, md5


class FuncCache:

    def __init__(self, cache=None, key_prefix=None, params_encoder_cls=None):
        self.cache = cache
        self.key_prefix = key_prefix
        self.params_encode_cls = None

    # 可以自定义生成key的方式
    def gen_key(self, func):
        fname = function_namespace(func)
        params = unpack_params_to_dict(func, args, kwargs)
        sp = json.dumps(params, sort_key=True, cls=self.params_encoder_cls)
        origin_s = '{}:{}'.format(fname, sp)
        key = md5(origin_s)
        if self.key_prefix:
            key = self.key_prefix + key
        return key

    def memoize(func):
        def wrapper(*args, **kwargs):
            cache_key = self.gen_key(func, args, kwargs)
            rv = self.cache.get(key)
            if rv is None:
                rv = func(*args, **kwargs)
                # TODO: 需要设置timeout
                if self.before_set_cache:
                    self.before_set_cache(func, args, kwargs, cache_key, rv)
                self.cache.set(
                    cache_key, rv,
                    timeout=10
                )
            return rv
        return wrapper


    def aio_memoize(func):
        async def wrapper(*args, **kwargs):
            cache_key = self.gen_key(func, args, kwargs)
            rv = await self.cache.get(key)
            if rv is None:
                rv = await func(*args, **kwargs)
                # TODO: 需要设置timeout
                if self.before_set_cache:
                    await self.before_set_cache(func, args, kwargs, cache_key, rv)

                await self.cache.set(
                    cache_key, rv,
                    timeout=10
                )
            return rv
        return wrapper
