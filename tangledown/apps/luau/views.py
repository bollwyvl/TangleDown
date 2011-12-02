from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext

from util.shortcuts import context_response

from luau.models import WikiPage
from luau.forms import WikiPageForm

def show_page(request, page_slug=None):
    """
    Show a WikiPage (or redirect to LUAU_DEFAULT_SLUG)
    """
    if not page_slug:
        return redirect('luau.views.show_page', page_slug=settings.LUAU_DEFAULT_SLUG)
        
    try:
        page = WikiPage.objects.get(name=page_slug)
    except WikiPage.DoesNotExist:
        return redirect('luau.views.edit_page', page_slug=page_slug)
    
    ctxt = dict(page=page) 
         
    return context_response(request, 'luau/show.html', ctxt)

def edit_page(request, page_slug=None):
    """
    Edit a WikiPage
    """
    try:
        page = WikiPage.objects.get(name=page_slug)
    except WikiPage.DoesNotExist:
        page = WikiPage(title=page_slug, name=page_slug)
    
    if request.POST.get('action', None) == 'edit':
        form = WikiPageForm(request.POST, instance=page)
        if form.is_valid():
            form.instance.save()
            return redirect('luau.views.show_page', page_slug=page_slug)
        else:
            return context_response(request, 'luau/edit.html', {'form':form})
    
    ctxt = dict(
        form=WikiPageForm(instance=page),
        page=page,
        )
    
    return context_response(request, 'luau/edit.html', ctxt)
 