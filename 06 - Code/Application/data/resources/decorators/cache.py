import redis
from config import settings

my_cache_host = settings.get_cache_options()['host']
my_cache_port = settings.get_cache_options()['port']


# Eventually will want redis to be a pipe that stays open, but will connect every time for now.
def cache_response(expire):
    def decorator(func):
        def func_wrapper(*args, **kwargs):
            req = args[1]
            res = args[2]
            r = redis.StrictRedis(host=my_cache_host, port=my_cache_port, db=0)

            if r.get(req.path) is None:
                print('create new stash')
                f = func(*args, **kwargs)
                value = res.body
                r.set(req.path, value)
                r.expire(req.path, expire)
                return f
            else:
                print('retrieve old stash')
                res.body = r.get(req.path)

            return None
        return func_wrapper
    return decorator


def cache_delete(also_delete=None):
    def decorator(func):
        def func_wrapper(*args, **kwargs):
            req = args[1]
            # res = args[2]
            r = redis.StrictRedis(host=my_cache['host'], port=my_cache['port'], db=0)
            delete(r, req.path)

            if also_delete is not None:
                for path in also_delete:
                    delete(r, path)

            return func(*args, **kwargs)
        return func_wrapper
    return decorator


def delete(r, path):
    if r.exists(path):
        print("I am deleting {0}".format(path))
        r.delete(path)
