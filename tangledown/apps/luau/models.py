from django.db import models
import re

VARS_PAT = re.compile(r'^\[.*\]: #(?P<var>[^:]*)(?P<rest>.*)', re.MULTILINE)
REST_PAT = re.compile(r'(?P<mod>[^:]*)=(?P<val>[^:]*)')

# Create your models here.
class WikiPage(models.Model):
    """A wiki page"""
    title = models.CharField(blank=False, max_length=100, unique=True)
    name = models.SlugField(unique=True, max_length=100,
        help_text="A short, unique name: no spaces!")
    body = models.TextField(blank=True,
        help_text="The page body, with Markdown and TangleDown")


    def __unicode__(self):
        return u"%s" % self.name
        
    
    def tangle_initialize(self):
        result = []
        
        for var, mods in self.tangled_body.items():
            if 'init' in mods:
                result.append('this.%s = %s;' % (
                    var, mods['init'][0].replace('#','this.')
                    ))
        return "\n".join(result)

    def tangle_update(self):
        # TODO: BOO! work with any TK control
        templ = """
        if(!$('.TKAdjustableNumberDown.tangledown_%(var)s').length){
            this.%(var)s = %(constraint)s;
        }"""
        result = []
        for var, mods in self.tangled_body.items():
            for constraint in mods.get('constraint', []):
                result.append(templ % dict(
                    var=var, 
                    constraint=constraint.replace('#','this.')
                    ))
        
        return "\n".join(result)
        
    @property
    def tangled_body(self):
        """
        returns a parsed version of all found variables:
        {
            'cookies': {
                'init': [0],
                'constraint': [
                    '#calories/50',
                ],
            }
        }
        
        """
        result = {}
        for var in [m.groupdict() for m in VARS_PAT.finditer(self.body)]:
            result[var['var'].strip()] = {}
            for mod in [m.groupdict() for m in REST_PAT.finditer(var['rest'])]:
                result[var['var']].setdefault(mod['mod'],[]).append(mod['val'].strip())
        return result