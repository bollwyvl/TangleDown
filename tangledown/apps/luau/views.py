from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.conf import settings
from django.template import RequestContext
from django.template.defaultfilters import slugify

from util.shortcuts import context_response

from luau.models import WikiPage
from luau.forms import WikiPageForm

def show_page(request, page_slug=None):
    """
    Show a WikiPage (or redirect to LUAU_DEFAULT_SLUG)
    """
    
    if not page_slug:
        page_slug = slugify(request.GET.get('new', settings.LUAU_DEFAULT_SLUG))
        title = request.GET.get('title', request.GET.get('new', settings.LUAU_DEFAULT_SLUG))
        try:
            page = WikiPage.objects.get(name=page_slug)
            return redirect('/wiki/%s' % (page_slug))
        except WikiPage.DoesNotExist:
            return redirect('/wiki/%s?title=%s' % (page_slug, title))
        
    try:
        page = WikiPage.objects.get(name=page_slug)
    except WikiPage.DoesNotExist:
        title = request.GET.get('title', page_slug)
        return redirect('/wiki/%s/edit?title=%s' % (page_slug, title))
    
    ctxt = dict(
        page=page,
        pages=WikiPage.objects.all(),
    )
         
    return context_response(request, 'luau/show.html', ctxt)

def edit_page(request, page_slug=None):
    """
    Edit a WikiPage
    """
    try:
        page = WikiPage.objects.get(name=page_slug)
    except WikiPage.DoesNotExist:
        page = WikiPage(name=page_slug, title=request.GET.get('title', page_slug))
    
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
        pages=WikiPage.objects.all(),
        )
    
    return context_response(request, 'luau/edit.html', ctxt)
 