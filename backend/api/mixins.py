from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin, UpdateModelMixin)
from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED




class ListCreateRetrieveMixin(ListModelMixin,
                              CreateModelMixin,
                              RetrieveModelMixin):
    pass
