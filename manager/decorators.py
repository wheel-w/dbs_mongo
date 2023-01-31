import uuid
from functools import wraps

from manager.models import OperationRecord


def operation_record(view_func):
    def wrapped_view(request, *args, **kwargs):
        record = {
            "instance_id": kwargs.get("pk"),
            "trace_id": uuid.UUID(request.trace_id),
            "api_name": request.resolver_match.view_name,
            "api_data": {**request.data, **request.query_params},
            "api_response": "success",
        }
        OperationRecord.objects.create(**record)
        view_func(request, *args, **kwargs)

    return wraps(view_func)(wrapped_view)


def operation_fail_record(view_func):
    def wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        if isinstance(response.data, str):
            OperationRecord.objects.filter(trace_id=uuid.UUID(request.trace_id)).update(api_response=response.data)
        return response

    return wraps(view_func)(wrapped_view)
