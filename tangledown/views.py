from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext

from util.shortcuts import context_response

from luau.models import WikiPage

from tangle.markdown import mdx_tangle

def home(request):
    ctxt = {
        'sample': WikiPage.objects.get(name='home'),
    }
    
    
    return context_response(request, 'homepage.html', ctxt)