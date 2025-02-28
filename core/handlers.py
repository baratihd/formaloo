from django.views.defaults import (
    bad_request,
    server_error,
    page_not_found,
    permission_denied,
)

from rest_framework.views import exception_handler as core_exception_handler


def exception_handler(exc, context):
    return core_exception_handler(exc, context)


def error400(request, exception, *args, **kwargs):
    return bad_request(request, exception, *args, **kwargs)


def error403(request, exception, *args, **kwargs):
    return permission_denied(request, exception, *args, **kwargs)


def error404(request, exception, *args, **kwargs):
    return page_not_found(request, exception, *args, **kwargs)


def error500(request, *args, **kwargs):
    return server_error(request, *args, **kwargs)
