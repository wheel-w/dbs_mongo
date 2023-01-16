import uuid
from functools import wraps

from manager.models import OperationRecord


def operation_record(view_func):
    """Mark a view function as being exempt from login view protection"""

    def wrapped_view(request, *args, **kwargs):
        record = {
            "instance_id": kwargs.get("pk"),
            "trace_id": uuid.UUID(request.trace_id),
            "api_name": request.resolver_match.view_name,
            "api_data": request.body,
        }
        response = view_func(request, *args, **kwargs)
        record["api_response"] = response.data
        OperationRecord.objects.create(**record)
        return response

    return wraps(view_func)(wrapped_view)
