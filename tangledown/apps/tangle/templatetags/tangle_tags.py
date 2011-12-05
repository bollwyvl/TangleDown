import re 

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Context
from django.template.loader import get_template
from django import template

import markdown

from util.decorators import memoized
from util.json_encode import json_encode

register = template.Library()

STRIP_CODE = re.compile(r'<pre><code class="(update|initialize|equations)">.*?</code></pre>', re.M | re.S)

@register.simple_tag(takes_context=True)
def tangle_imports(context):
    template = get_template("tangle/tangle_imports.html")
    return template.render(context)
    
@register.simple_tag(takes_context=True)
def tangledown(context, tangleable):
    return re.sub(STRIP_CODE, '',
                  markdown.markdown(tangleable, extensions=['tangle', 'fenced_code'])
                  )


@register.simple_tag(takes_context=True)
def tangle_instance(context, tangleable, root):
    template = get_template("tangle/tangle_instance.html")
    c = Context(dict(
        root=root,
        using_sympy=False,
    ))
    if using_sympy(tangleable):
        c.update(dict(
            initialize=tangle_initialize(tangleable),
            constraints=json_encode(tangle_sympy_constraints(tangleable)),
            using_sympy=True,
            ))
    else:
        c.update(dict(
            initialize=tangle_initialize(tangleable),
            update=tangle_update(tangleable),
            ))
    return template.render(c)

def using_sympy(tangleable):
    return bool(len(list(get_code_lines(tangleable, 'equations'))))

def get_code_lines(tangleable, stage):
    for cb in tangle_tree(tangleable).findall('*/code'):
        if stage in cb.get('class', ''):
            for line in cb.text.split('\n'):
                line.strip()
                if line:
                    yield line

def jsify(line):
    return line.replace('#','this.').replace(':','=')+";"

def tangle_initialize(tangleable):
    return "\n".join(map(jsify, get_code_lines(tangleable, 'initialize')))

def tangle_update(tangleable):
    return "\n".join(map(jsify, get_code_lines(tangleable, 'update')))
    
def tangle_sympy_constraints(tangleable):
    lines = [[h.strip() for h in line.split(':')] for line in get_code_lines(tangleable, 'equations')]
    return lines
    
@memoized
def tangle_tree(tangleable):
    """
    TODO: at some point, Markdown must have the tree available, and 
          we shouldn't have to reparse to get it
    """
    md = markdown.Markdown(extensions=['tangle', 'fenced_code'])
    html = md.convert(tangleable)
    return markdown.util.etree.XML('<body>%s</body>' % html)