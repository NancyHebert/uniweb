import falcon
import re


# Todo: Make this manage a dictionary of matches.
def rematch(arg_name, match_type):
    def decorator(func):
        def func_wrapper(*args, **kwargs):
            my_pattern = re.compile(match_type)
            if not my_pattern.match(kwargs[arg_name]):
                raise falcon.HTTPError(falcon.HTTP_400,
                                       'Type Error',
                                       '{} does not match the pattern <{}>'.format(kwargs[arg_name], match_type))
            return args, kwargs
        return func_wrapper
    return decorator
