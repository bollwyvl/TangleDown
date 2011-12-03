import re 

from django.template import Context
from django.template.loader import get_template
from django import template

import markdown

register = template.Library()

STRIP_CODE = re.compile(r'<pre><code class="(update|initialize)">.*?</code></pre>', re.M | re.S)

@register.simple_tag(takes_context=True)
def tangle_imports(context):
    template = get_template("tangle/tangle_imports.html")
    return template.render(context)

@register.simple_tag(takes_context=True)
def tangle_instance(context, tangleable, root):
    template = get_template("tangle/tangle_instance.html")
    c = Context(dict(
        root=root,
        tangleable=tangleable,
    ))
    return template.render(c)
    
@register.simple_tag(takes_context=True)
def tangledown(context, text):
    return re.sub(STRIP_CODE, '',
                  markdown.markdown(text, extensions=['tangle', 'fenced_code'])
                  )
