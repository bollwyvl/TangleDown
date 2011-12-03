#!/usr/bin/env python

"""
Embeds Tangle reactive elements

All resulting HTML is XHTML Strict compatible.

Examples:

>>> import markdown
>>> md = markdown.Markdown(extensions=['tangle'])

Good ol' adjustable number

>>> md.convert("t[number](cookies)")
u'<p><span class="TKAdjustableNumber" data-var="cookies"></span></p>'

>>> md.convert("t[number](0<percentCompliance..5<100 percent '%')")
u'<p><span class="TKAdjustableNumber" data-format="percent" data-max="100" data-min="0" data-step="5" data-var="percentCompliance">%</span></p>'

>>> md.convert('t[number](0<percentCompliance..5<100 percent "%")')
u'<p><span class="TKAdjustableNumber" data-format="percent" data-max="100" data-min="0" data-step="5" data-var="percentCompliance">%</span></p>'


Plain ol' number field

>>> md.convert('t[field](cookies " cookies")')
u'<p><span class="TKNumberField" data-var="cookies"> cookies</span></p>'

>>> md.convert('t[field 5](cookies " cookies")')
u'<p><span class="TKNumberField" data-size="5" data-var="cookies"> cookies</span></p>'

>>> md.convert('t[field]( cookies )')
u'<p><span class="TKNumberField" data-var="cookies"></span></p>'

The toggle

>>> md.convert('t[toggle](newAdmissionAppliesToEveryone)[those who paid the charge][everyone]')
u'<p><span class="TKToggle" data-var="newAdmissionAppliesToEveryone"><span>those who paid the charge</span><span>everyone</span></span></p>'

"""
import re

import markdown

version = "0.0"

def makeExtension(configs=None) :
    return TangleExtension(configs=configs)
    
class TangleExtension(markdown.Extension):
    tangle_inline_classes = []
    
    def __init__(self, configs):
        self.config = {
            #TODO: meh?
        }
        

        # Override defaults with user settings
        for key, value in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        for cls in self.tangle_inline_classes:
            md.inlinePatterns.add(cls.__name__, cls(cls.find_pattern, md), "<reference")


def tk_span(cls, text=None, ignore=[], children=[], **kwargs):
    """
    Helper function. Creates the "normal" TangleKit spans.
    """
    kwargs = dict([('data-'+k, v) for k, v in kwargs.items() if v not in [None,""] and k not in ignore])
    obj = markdown.util.etree.Element('span')
    [obj.append(c) for c in children]
    if text:
        obj.text = text
    obj.set('class', cls.__class__.__name__)
    [obj.set(k, v) for k, v in kwargs.items()]
    return obj


class TKToggle(markdown.inlinepatterns.Pattern):
    find_pattern = r't\[toggle\]\((?P<var>[^\)]*)\)\[(?P<op0>[^\]]*)\]\[(?P<op1>[^\]]*)\]'
    
    def handleMatch(self, m):
        kwargs = {}
        children = []
        text = ""
        bits = m.groupdict()
        for op_text in [bits['op0'], bits['op1']]:
            op = markdown.util.etree.Element('span')
            op.text = op_text
            children.append(op)
        kwargs = bits
        return tk_span(self, children=children, ignore=['op0', 'op1'], **kwargs)
        
TangleExtension.tangle_inline_classes.append(TKToggle)


class TKNumberField(markdown.inlinepatterns.Pattern):
    find_pattern = r't\[field( (?P<size>\d*))?\]\((?P<stuff>[^\)]*)\)'
    stuff_pattern = re.compile(r'''
        \s*
        (?P<var>[^ ]*)           #required variable
        \s*                       #maybe some spaces
        (([\"\'])
        (?P<label>[^\3]*)         #optional quoted label
        \3|$)
        \s*
        ''', re.X)
        
    def handleMatch(self, m):
        bits = self.stuff_pattern.match(m.groupdict()['stuff'])
        kwargs = {}
        text = ""
        if bits:
            bits = bits.groupdict()
            if m.groupdict()['size']:
                bits['size'] = m.groupdict()['size']
            text = bits['label']
            kwargs = bits
        return tk_span(self, text, ignore=['label'], **kwargs)

TangleExtension.tangle_inline_classes.append(TKNumberField)


class TKAdjustableNumber(markdown.inlinepatterns.Pattern):
    find_pattern = r't\[number\]\((?P<stuff>[^\)]*)\)'
    stuff_pattern = re.compile(r'''
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
        bits = self.stuff_pattern.match(m.groupdict()['stuff'])
        kwargs = {}
        text = ""
        if bits:
            bits = bits.groupdict()
            text = bits['label']
            kwargs = bits
        return tk_span(self, text, ignore=['label', 'qt'], **kwargs)
        
TangleExtension.tangle_inline_classes.append(TKAdjustableNumber)


if __name__ == "__main__":
    import doctest
    doctest.testmod()