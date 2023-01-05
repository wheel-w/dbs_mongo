import uuid

from common.utils import local


class TraceIDInjectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.trace_id = uuid.uuid4().hex
        local.set_trace_id(request.trace_id)
        response = self.get_response(request)
        return response
