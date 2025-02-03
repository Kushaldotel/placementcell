from rest_framework.compat import (
    INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS)
from rest_framework.renderers import JSONRenderer
from rest_framework.utils import json


def get_message(response):
    status_code = response.status_code
    response_message = getattr(response, 'message', None)
    if response_message:
        return response_message
    if 200 <= status_code <= 300:
        return 'Successful'
    return 'Error. See details'


class CustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
            Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return b''

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS
        is_paginated = False
        if hasattr(renderer_context.get('view'), 'pagination_class'):
            is_paginated = getattr(renderer_context.get('view'), 'pagination_class') is not None
        data_dict = dict(
            success=200 <= renderer_context.get('response').status_code <= 300,
            message=get_message(renderer_context.get('response')),
            is_paginated=is_paginated,
            data=data
        )
        ret = json.dumps(
            data_dict, cls=self.encoder_class,
            indent=indent, ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict, separators=separators
        )

        # We always fully escape \u2028 and \u2029 to ensure we output JSON
        # that is a strict javascript subset.
        # See: http://timelessrepo.com/json-isnt-a-javascript-subset
        ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
        return ret.encode()


def create_response(success, message, data):
    return dict(success=success, message=message, data=data)