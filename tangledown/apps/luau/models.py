from django.db import models
import re
import markdown

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
        
    def get_code_lines(self, stage):
        for cb in self.tangled_body.findall('*/code'):
            if stage in cb.get('class'):
                for var_init in cb.text.split('\n'):
                    var_init = var_init.strip()
                    if var_init.startswith('#'):
                        yield var_init.replace('#','this.').replace(':','=')+";"
    
    def tangle_initialize(self):
        return "\n".join(self.get_code_lines('initialize'))

    def tangle_update(self):
        return "\n".join(self.get_code_lines('update'))
        
    @property
    def tangled_body(self):
        
        if not hasattr(self,"_tangled_body"):
            md = markdown.Markdown(extensions=['tangle', 'fenced_code'])
            html = md.convert(self.body)
            self._tangled_body = markdown.util.etree.XML('<body>%s</body>' % html)
            
        return self._tangled_body