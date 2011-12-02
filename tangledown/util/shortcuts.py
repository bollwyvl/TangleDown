from django.shortcuts import render_to_response
from django.template import RequestContext

def context_response(req, *args, **kwargs):
    kwargs['context_instance'] = RequestContext(req)
    return render_to_response(*args, **kwargs)