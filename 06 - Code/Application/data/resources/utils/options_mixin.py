"""
A mixin to be added to each resource to provide an on_options method.
Avoids code duplication. Every resource that includes this mixin will support
the HTTP options verb.
"""

allow_enum = {
    'on_get': 'GET',
    'on_post': 'POST',
    'on_put': 'PUT',
    'on_patch': 'PATCH',
    'on_head': 'HEAD',
    'on_options': 'OPTIONS',
    'on_delete': 'DELETE'
}


class OptionMixin(object):
    def on_options(self, req, resp, *args, **kwargs):
        my_methods = dir(self)
        allow_header = ""
        for each_method in allow_enum.keys():
            if each_method in my_methods:
                allow_header += allow_enum[each_method] + ','
        resp.append_header('allow', allow_header[:-1]) # trim trailing comma