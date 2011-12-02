from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext

from util.shortcuts import context_response

from luau.models import WikiPage

def home(request):
    ctxt = {}
    
    ctxt['sample'] = WikiPage.objects.order_by('?')[0]
    
    return context_response(request, 'homepage.html', ctxt)