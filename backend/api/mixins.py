from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


class PartialUpdateOnlyMixin(UpdateModelMixin):
    """
    Allows PATCH requests but not PUT requests.
    """

    def update(self, request, *args, **kwargs):
        if request.method == "PUT":
            return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
        return super().update(request, *args, **kwargs)


class ListCreateRetrieveMixin(ListModelMixin,
                              CreateModelMixin,
                              RetrieveModelMixin):
    """
    Allows GET and POST requests only.
    """

    pass
