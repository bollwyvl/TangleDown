#!/usr/bin/env python

"""
Embeds Tangle reactive elements

All resulting HTML is XHTML Strict compatible.

Examples:

>>> import markdown
>>> md = markdown.Markdown(extensions=['tangle', 'fenced_code', 'def_list])

## Good ol' adjustable number

>>> md.convert("t[number](cookies)")
u'<p><span class="TKAdjustableNumber" data-var="cookies"></span></p>'

>>> md.convert("t[number](0<percentCompliance..5<100 percent '%')")
u'<p><span class="TKAdjustableNumber" data-format="percent" data-max="100" data-min="0" data-step="5" data-var="percentCompliance">%</span></p>'

>>> md.convert('t[number](0<percentCompliance..5<100 percent "%")')
u'<p><span class="TKAdjustableNumber" data-format="percent" data-max="100" data-min="0" data-step="5" data-var="percentCompliance">%</span></p>'


## Plain ol' number field

>>> md.convert('t[field](cookies " cookies")')
u'<p><span class="TKNumberField" data-var="cookies"> cookies</span></p>'

>>> md.convert('t[field 5](cookies " cookies")')
u'<p><span class="TKNumberField" data-size="5" data-var="cookies"> cookies</span></p>'

>>> md.convert('t[field]( cookies )')
u'<p><span class="TKNumberField" data-var="cookies"></span></p>'

## The toggle

>>> md.convert('t[toggle](newAdmissionAppliesToEveryone)[those who paid the charge][everyone]')
u'<p><span class="TKToggle" data-var="newAdmissionAppliesToEveryone"><span>those who paid the charge</span><span>everyone</span></span></p>'

>>> md.convert('t[toggle]( newAdmissionAppliesToEveryone )[ those who paid the charge ][ everyone ]')
u'<p><span class="TKToggle" data-var="newAdmissionAppliesToEveryone"><span>those who paid the charge</span><span>everyone</span></span></p>'

## Oy. The empty case. Just shows a number

>>> md.convert('__t[](calories " calories")__')
u'<p><strong><span data-var="calories"> calories</span></strong></p>'

>>> md.convert('t[](restorationTime)')
u'<p><span data-var="restorationTime"></span></p>'

>>> md.convert('t[](surplus e6)')
u'<p><span data-format="e6" data-var="surplus"></span></p>'


## The Positive(or 0)/Negative switch

>>> md.convert('t[posneg](deltaBudget)[collect an extra][lose]')
u'<p><span class="TKSwitchPositiveNegative" data-var="deltaBudget"><span>collect an extra</span><span>lose</span></span></p>'

## The evil huge switch. Probably need to support this format for others.

>>> md.convert('''t[switch](scenarioIndex)
... |   This is not sufficient to maintain the parks, and t[](closedParkCount) 
...     parks would be shut down at least part-time.
...     
... |   This is sufficient to maintain the parks in their current state, but 
...     not fund a program to bring safety and cleanliness up to acceptable 
...     standards.
...     
... |   This is sufficient to maintain the parks in their current state, plus 
...     fund a program to bring safety and cleanliness up to acceptable standards 
...     over the next t[](restorationTime) years.
...     
... |   This is sufficient to maintain the parks and bring safety and cleanliness
...     up to acceptable standards, leaving a $t[](surplus e6) million per year 
...     surplus''')
u'<span class="TKSwitch" data-var="scenarioIndex"><span class="TKBranchOption">This is not sufficient to maintain the parks, and <span data-var="closedParkCount"></span> \\nparks would be shut down at least part-time.</span><span class="TKBranchOption">This is sufficient to maintain the parks in their current state, but \\nnot fund a program to bring safety and cleanliness up to acceptable \\nstandards.</span><span class="TKBranchOption">This is sufficient to maintain the parks in their current state, plus \\nfund a program to bring safety and cleanliness up to acceptable standards \\nover the next <span data-var="restorationTime"></span> years.</span><span class="TKBranchOption">This is sufficient to maintain the parks and bring safety and cleanliness\\nup to acceptable standards, leaving a $<span data-format="e6" data-var="surplus"></span> million per year \\nsurplus</span></span>'


>>> md.convert('''t[if](scenarioIndex)
... ~   This is not sufficient to maintain the parks, and t[](closedParkCount) 
...     parks would be shut down at least part-time.''')
u'<span class="TKIf" data-var="scenarioIndex"><span class="TKBranchOption">This is not sufficient to maintain the parks, and <span data-var="closedParkCount"></span> \\nparks would be shut down at least part-time.</span></span>'

>>> md.convert('''t[if]( scenarioIndex invert )
... ~   This is not sufficient to maintain the parks, and t[](closedParkCount) 
...     parks would be shut down at least part-time.''')
u'<span class="TKIf" data-invert="true" data-var="scenarioIndex"><span class="TKBranchOption">This is not sufficient to maintain the parks, and <span data-var="closedParkCount"></span> \\nparks would be shut down at least part-time.</span></span>'

>>> md.convert('''t[if]( scenarioIndex invert )
... ~   This is not sufficient to maintain the parks, and t[](closedParkCount) 
...     parks would be shut down at least part-time.
...
... t[switch](scenarioIndex)
... |    Foo
... |    Bar''')
u'<span class="TKIf" data-invert="true" data-var="scenarioIndex"><span class="TKBranchOption">This is not sufficient to maintain the parks, and <span data-var="closedParkCount"></span> \\nparks would be shut down at least part-time.</span></span><span class="TKSwitch" data-var="scenarioIndex"><span class="TKBranchOption">Foo</span><span class="TKBranchOption">Bar</span></span>'


>>> md.convert('''If you eat t[number](cookies ' cookies'), you consume t[](calories ' calories'). 
... This constitutes t[](dailypercent  '%') of a daily intake of t[number](dailycalories 'calories').
...
... ~~~~.initialize
... #cookies = 3
... #calories = 150
... #dailypercent = 1
... #dailycalories = 2100
... ~~~~
...
... ~~~~.update
... #calories = #cookies * 50
... #dailypercent  = (#cookies * 50) / #dailycalories
... ~~~~''')
u'foo'

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
            
        """ Add an instance of DefListProcessor to BlockParser. """
        md.parser.blockprocessors.add('tkswitchlist', 
                                      TKSwitchProcessor(md.parser),
                                      '>ulist')
        md.parser.blockprocessors.add('tkif', 
                                      TKIfProcessor(md.parser),
                                      '>ulist')

def tk_span(cls_or_class, text=None, ignore=[], children=[], **kwargs):
    """
    Helper function. Creates the "normal" TangleKit spans.
    """
    kwargs = dict([('data-'+k, v) for k, v in kwargs.items() if v not in [None,""] and k not in ignore])
    obj = markdown.util.etree.Element('span')
    [obj.append(c) for c in children]
    if text:
        obj.text = text
    if isinstance(cls_or_class, str):
        obj.set('class', cls_or_class)
    else:
        obj.set('class', cls_or_class.__class__.__name__)
    [obj.set(k, v) for k, v in kwargs.items()]
    return obj

class TKBranchingProcessor(markdown.blockprocessors.BlockProcessor):
    """
    Process Definition Lists.
    
    Shamelessly plundered from markdown.extensions.deflist... should work together, though.
    
    TODO: Nesting?
    """

    RE = re.compile(r'(^|\n)[ ]{0,3}\|[ ]{1,3}(.*?)(\n|$)')
    NO_INDENT_RE = re.compile(r'^[ ]{0,3}[^ \|]')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        terms = [l.strip() for l in block[:m.start()].split('\n') if l.strip()]
        block = block[m.end():]
        no_indent = self.NO_INDENT_RE.match(block)
        if no_indent:
            d, theRest = (block, None)
        else:
            d, theRest = self.detab(block)
        if d:
            d = '%s\n%s' % (m.group(2), d)
        else:
            d = m.group(2)
        sibling = self.lastChild(parent)
        if not terms and sibling.tag == 'p':
            # The previous paragraph contains the terms
            state = 'looselist'
            terms = sibling.text.split('\n')
            parent.remove(sibling)
            # Aquire new sibling
            sibling = self.lastChild(parent)
        else:
            state = 'list'

        if sibling and sibling.get('class') == self.tree_class:
            # This is another item on an existing list
            dl = sibling
            if len(dl) and dl[-1].get('class') == 'TKBranchOption' and len(dl[-1]):
                state = 'looselist'
        else:
            # This is a new list
            dl = markdown.util.etree.SubElement(parent, 'span')
            dl.set("class", self.tree_class)
        # Add terms
        for term in terms:
            self.term_handler(dl, term)
        # Add definition
        self.parser.state.set(state)
        dd = markdown.util.etree.SubElement(dl, 'span')
        dd.set('class', 'TKBranchOption')
        self.parser.parseBlocks(dd, [d])
        self.parser.state.reset()

        if theRest:
            blocks.insert(0, theRest)
    
class TKSwitchProcessor(TKBranchingProcessor):
    tree_class = 'TKSwitch'
    RE = re.compile(r'(^|\n)[ ]{0,3}\|[ ]{1,3}(.*?)(\n|$)')
    
    def term_handler(self, tree, term):
        term_match = re.match(r't\[switch\]\(\s*(?P<var>[^\)\s]*)\s*\)', term)
        if term_match:
            tree.set('data-var', term_match.groupdict()['var'])

class TKIfProcessor(TKBranchingProcessor):
    tree_class = 'TKIf'
    RE = re.compile(r'(^|\n)[ ]{0,3}\~[ ]{1,3}(.*?)(\n|$)')
    
    def term_handler(self, tree, term):
        term_match = re.match(r't\[if\]\(\s*(?P<var>[^\) ]*)\s*(?P<invert>invert)?\s*\)', term)
        if term_match:
            tree.set('data-var', term_match.groupdict()['var'])
            if term_match.groupdict()['invert']:
                tree.set('data-invert', 'true')


class TKVoid(markdown.inlinepatterns.Pattern):
    find_pattern = r't\[\]\((?P<stuff>[^\)]*)\)'
    stuff_pattern = re.compile(r'''
        \s*
        (?P<var>[^\. ]*)          #required variable
        \s*                       #maybe some space
        (?P<format>[^\"\'\s]*)    #optional sprintf format
        \s*                       #maybe some spaces
        ((?P<qt>[\"\'])
        (?P<label>[^\4]*)        #optional quoted label
        \4|$)
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
        return tk_span(None, text, ignore=['qt','label'], **kwargs)
        
TangleExtension.tangle_inline_classes.append(TKVoid)


class TKToggle(markdown.inlinepatterns.Pattern):
    find_pattern = r't\[toggle\]\(\s*(?P<var>[^\)\s]*)\s*\)\[\s*(?P<op0>[^\]]*[^\s])\s*\]\[\s*(?P<op1>[^\]]*[^\s])\s*\]'
    
    def handleMatch(self, m):
        kwargs = {}
        children = []
        text = ""
        bits = m.groupdict()
        kwargs['var'] = bits['var']
        for op_text in [bits['op0'], bits['op1']]:
            op = markdown.util.etree.Element('span')
            op.text = op_text
            children.append(op)
        kwargs = bits
        return tk_span('TKToggle TKSwitch', children=children, ignore=['op0', 'op1'], **kwargs)
        
TangleExtension.tangle_inline_classes.append(TKToggle)


class TKSwitchPositiveNegative(TKToggle):
    find_pattern = r't\[posneg\]\(\s*(?P<var>[^\)\s]*)\s*\)\[\s*(?P<op0>[^\]]*[^\s])\s*\]\[\s*(?P<op1>[^\]]*[^\s])\s*\]'

TangleExtension.tangle_inline_classes.append(TKSwitchPositiveNegative)


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
        (?P<var>[^\. ]*)          #required variable
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