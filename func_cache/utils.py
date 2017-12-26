# -*- coding: utf-8 -*-
import inspect


def md5(s):
    if isinstance(s, str):
        s = s.encode()
    return hashlib.md5(s).hexdigest()


def function_namespace(func):
    return '{}.{}'.format(func.__module__, func.__qualname__)


def unpack_params_to_dict(func, args, kw):
    """将func的参数和默认参数封装到一个dict中去"""
    kw = kw.copy()
    sig = inspect.signature(func)
    result = {}
    for i, p in enumerate(sig.parameters.values()):
        if p.name in kw:
            result[p.name] = kw.pop(p.name)
            continue
        if p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD:
            if len(args) > i:
                result[p.name] = args[i]
            else:
                result[p.name] = p.default
        elif p.kind == inspect.Parameter.VAR_POSITIONAL:
            result[p.name] = args[i:]
        elif p.kind == inspect.Parameter.KEYWORD_ONLY:
            result[p.name] = p.default
        elif p.kind == inspect.Parameter.VAR_KEYWORD:
            result[p.name] = kw
    return result
