#!/usr/bin/env python

"""
Embeds Tangle reactive elements

All resulting HTML is XHTML Strict compatible.

Examples:

>>> import markdown
>>> md = markdown.Markdown(extensions=['tangle'])
>>> md.convert("t<number](0<percentCompliance..5<100 percent '%')")
u'<p><span class="TKAdjustableNumber" data-format="percent" data-max="100" data-min="0" data-step="5" data-var="percentCompliance">%</span></p>'

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
           TKAdjustableNumber:  r't<number\]\((?P<stuff>[^\)]*)\)',
        }
        
        for cls, pat in pats.items():
            md.inlinePatterns.add(cls.__name__, cls(pat, md), "<reference")

class TKAdjustableNumber(markdown.inlinepatterns.Pattern):
    patt = re.compile(r'''
        ((?P<min>[\d\-.]*)<|)     #optional minimum
        (?P<var>[^\.]*)           #required variable
        (\.\.(?P<step>[\d\-.]*)|) #optional step
        (<(?P<max>[\d\-.]*)|)     #optional maximum
        \s*                       #maybe some space
        (?P<format>[^\"\'\s]*)    #optional sprintf format
        \s*                       #maybe some spaces
        ((?P<qt>[\"\'])
        (?P<label>[^\10]*)         #optional quoted label
        \10|$)                    
                              ''', re.X)
    def handleMatch(self, m):
        bits = self.patt.match(m.groupdict()['stuff'])
        kwargs = {}
        text = ""
        if bits:
            bits = bits.groupdict()
            #{'qt': "'", 'min': '0', 'max': '100', 'fmt': 'percent', 'label': '%', 'step': '5', 'var': 'percentCompliance'}
            del(bits['qt'])
            text = bits['label']
            del(bits['label'])
            kwargs = dict([('data-'+k, v) for k, v in bits.items()])
        return tk_span(self, text, **kwargs)

def tk_span(cls, text, **kwargs):
    obj = markdown.util.etree.Element('span')
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