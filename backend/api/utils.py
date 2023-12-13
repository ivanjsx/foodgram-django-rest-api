from django.http import Http404, JsonResponse

from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    if isinstance(exc, Http404):
        return Response(data={"detail": "resource not found."},
                        status=HTTP_404_NOT_FOUND)
    return exception_handler(exc, context)


def custom_404_handler(request, exception):
    return JsonResponse(data={"detail": "resource not found."},
                        status=HTTP_404_NOT_FOUND)
