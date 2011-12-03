#!/usr/bin/env python

"""
Embeds Tangle reactive elements

All resulting HTML is XHTML Strict compatible.

Examples:

>>> import markdown
>>> md = markdown.Markdown(extensions=['tangle'])


>>> md.convert("t[number](cookies)")
u'<p><span class="TKAdjustableNumber" data-var="cookies"></span></p>'

>>> md.convert("t[number](0<percentCompliance..5<100 percent '%')")
u'<p><span class="TKAdjustableNumber" data-format="percent" data-max="100" data-min="0" data-step="5" data-var="percentCompliance">%</span></p>'

>>> md.convert('t[number](0<percentCompliance..5<100 percent "%")')
u'<p><span class="TKAdjustableNumber" data-format="percent" data-max="100" data-min="0" data-step="5" data-var="percentCompliance">%</span></p>'


>>> md.convert('t[field](cookies " cookies")')
u'<p><span class="TKNumberField" data-var="cookies"> cookies</span></p>'

>>> md.convert('t[field 5](cookies " cookies")')
u'<p><span class="TKNumberField" data-size="5" data-var="cookies"> cookies</span></p>'

>>> md.convert('t[field]( cookies )')
u'<p><span class="TKNumberField" data-var="cookies"></span></p>'

"""
import re

import markdown

version = "0.0"

class TangleExtension(markdown.Extension):
    def __init__(self, configs):
        self.config = {
            #TODO: meh?
        }

        # Override defaults with user settings
        for key, value in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        pats = {
           TKAdjustableNumber:  r't\[number\]\((?P<stuff>[^\)]*)\)',
           TKNumberField:  r't\[field( (?P<size>\d*))?\]\((?P<stuff>[^\)]*)\)',
        }
        
        for cls, pat in pats.items():
            md.inlinePatterns.add(cls.__name__, cls(pat, md), "<reference")

class TKNumberField(markdown.inlinepatterns.Pattern):
    patt = re.compile(r'''
        \s*
        (?P<var>[^ ]*)           #required variable
        \s*                       #maybe some spaces
        (([\"\'])
        (?P<label>[^\3]*)         #optional quoted label
        \3|$)
        \s*
        ''', re.X)
    def handleMatch(self, m):
        bits = self.patt.match(m.groupdict()['stuff'])
        kwargs = {}
        text = ""
        if bits:
            bits = bits.groupdict()
            if m.groupdict()['size']:
                bits['size'] = m.groupdict()['size']
            text = bits['label']
            del(bits['label'])
            kwargs = bits
        return tk_span(self, text, **kwargs)

class TKAdjustableNumber(markdown.inlinepatterns.Pattern):
    patt = re.compile(r'''
        \s*
        ((?P<min>[\d\-.]*)<|)     #optional minimum
        (?P<var>[^\.]*)           #required variable
        (\.\.(?P<step>[\d\-.]*)|) #optional step
        (<(?P<max>[\d\-.]*)|)     #optional maximum
        \s*                       #maybe some space
        (?P<format>[^\"\'\s]*)    #optional sprintf format
        \s*                       #maybe some spaces
        ((?P<qt>[\"\'])
        (?P<label>[^\10]*)        #optional quoted label
        \10|$)
        \s*                    
                              ''', re.X)
    def handleMatch(self, m):
        bits = self.patt.match(m.groupdict()['stuff'])
        kwargs = {}
        text = ""
        if bits:
            bits = bits.groupdict()
            del(bits['qt'])
            text = bits['label']
            del(bits['label'])
            kwargs = bits
        return tk_span(self, text, **kwargs)

def tk_span(cls, text=None, **kwargs):
    kwargs = dict([('data-'+k, v) for k, v in kwargs.items() if v not in [None,""]])
    obj = markdown.util.etree.Element('span')
    if text:
        obj.text = text
    obj.set('class', cls.__class__.__name__)
    [obj.set(k, v) for k, v in kwargs.items()]
    return obj

def makeExtension(configs=None) :
    return TangleExtension(configs=configs)


import markdown

if __name__ == "__main__":
    import doctest
    doctest.testmod()