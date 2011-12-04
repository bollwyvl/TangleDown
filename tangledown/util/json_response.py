from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse
from util.json_encode import *

class JsonResponse(HttpResponse):
    def __init__(self, object, float_precision=3):
        content = json_encode(object)
        super(JsonResponse, self).__init__(content, mimetype='application/json')
