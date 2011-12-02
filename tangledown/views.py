from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext

from util.shortcuts import context_response

def home(request):
    ctxt = {}
    ctxt['welcome'] = open('content/welcome.markdown').read()
    
    return context_response(request, 'homepage.html', ctxt)