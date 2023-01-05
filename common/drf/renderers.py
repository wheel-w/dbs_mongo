import json

from rest_framework.compat import INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS
from rest_framework.renderers import JSONRenderer

from common.utils import local


class StandardResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        renderer_context = renderer_context or {}
        renderer_context["response"].status_code = 200
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        # 如果请求失败,填充message信息
        if renderer_context["response"].exception:
            message = data
            render_data = {
                "result": False,
                "message": message,
                "code": -1,
                "data": None,
                "trace_id": local.get_trace_id(),
            }

        else:
            render_data = {
                "result": True,
                "message": "success",
                "code": 0,
                "data": data,
                "trace_id": local.get_trace_id(),
            }

        ret = json.dumps(
            render_data,
            cls=self.encoder_class,
            indent=indent,
            ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict,
            separators=separators,
        )

        ret = ret.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
        return ret.encode()
