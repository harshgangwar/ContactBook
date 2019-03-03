from __future__ import unicode_literals
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from contact.handlers import *


def response(status=HTTP_400_BAD_REQUEST, message=None, data=None):
    body = {
        'status': status,
        'message': message,
        'data': data
    }
    return Response(status=HTTP_200_OK, data=body)


class ContactViewSet(ViewSet):
    def list(self, request):
        status, message, data = ContactHandler.list(request)
        return response(status, message, data)

    def create(self, request):
        status, message, data = ContactHandler.create(request)
        return response(status, message, data)

    def partial_update(self, request, pk=None):
        status, message, data = ContactHandler.partial_update(request, pk)
        return response(status, message, data)
