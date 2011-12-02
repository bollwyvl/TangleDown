from django.template import Context
from django.template.loader import get_template
from django import template

register = template.Library()

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