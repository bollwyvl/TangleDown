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
STRIP_TABLE = re.compile(r'<table>.*?<thead>.*?<tr>.*?<th>#.*?</table>', re.M | re.S)


MD_EXTENSIONS = ['tangle', 'fenced_code', 'def_list', 'tables']

@register.simple_tag(takes_context=True)
def tangle_imports(context):
    template = get_template("tangle/tangle_imports.html")
    return template.render(context)
    
@register.simple_tag(takes_context=True)
def tangledown(context, tangleable):
    result = re.sub(STRIP_CODE, '',
                  markdown.markdown(tangleable, extensions=MD_EXTENSIONS)
                  )
    result = re.sub(STRIP_TABLE, '', result)
    return result


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

def generator_table_iter(fn, tangleable):
    tree = tangle_tree(tangleable)
    
    tables = tree.findall('.//table')
    
    for table in tables:
        ths = table.findall('.//th')
        if not filter(lambda t: t.text.startswith('#') == False, ths):
            yield "\n".join(fn(
                table, 
                [jsify(t.text, eol=False) for t in ths]
                ))


def _generator_inits(table, ths):
    for th in ths:
        yield "%s = [];" % th

def get_generator_inits(tangleable):
    return '\n'.join(generator_table_iter(_generator_inits, tangleable))

def _generator_tables(table, ths):
    trs = table.findall(".//tbody/tr")
    loop_guard = []
    loop_body = []
    for tr in range(len(trs)):
        tds = trs[tr].findall('td')
        for th in range(len(ths)):
            if tr == 0:
                yield '%s.push(%s);' % (
                    ths[th],
                    jsify(tds[th].text, eol=False),
                    )
            if tr == 1:
                loop_body.append('%s.push(%s[i] %s);' % (
                    ths[th],
                    ths[th],
                    jsify(tds[th].text, eol=False),
                    ))
            if tr == 2:
                if tds[th].text is not None:
                    loop_guard.append(
                        "(%s[i] %s)" % (
                            ths[th], 
                            jsify(tds[th].text, eol=False),
                            )
                    )
    yield '''var i = 0;
while(%s){
\t%s
i++;
}''' % ('||'.join(loop_guard), "\n\t".join(loop_body))
            
    
def get_generator_tables(tangleable):
    return '\n'.join(
        list(generator_table_iter(_generator_inits, tangleable)) + 
        list(generator_table_iter(_generator_tables, tangleable)))
            
def jsify(line, eol=True):
    if line is None:
        return ''
    return line.replace('#','this.').replace(':','=') + ["",";"][eol]

def tangle_initialize(tangleable):
    result = "\n".join(map(jsify, get_code_lines(tangleable, 'initialize')))
    result += get_generator_inits(tangleable)
    return result

def tangle_update(tangleable):
    result = "\n".join(map(jsify, get_code_lines(tangleable, 'update')))
    result += get_generator_tables(tangleable)
    return result
    
def tangle_sympy_constraints(tangleable):
    lines = [[h.strip() for h in line.split(':')] for line in get_code_lines(tangleable, 'equations')]
    return lines


@memoized
def tangle_tree(tangleable):
    """
    TODO: at some point, Markdown must have the tree available, and 
          we shouldn't have to reparse to get it
    """
    md = markdown.Markdown(extensions=MD_EXTENSIONS)
    html = md.convert(tangleable)
    return markdown.util.etree.XML('<body>%s</body>' % html)