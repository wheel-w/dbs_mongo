import logging

from common.utils import local


class TraceIDInjectFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        record.trace_id = local.get_trace_id()
        return True
