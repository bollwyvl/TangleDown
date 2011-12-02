from django.db import models

# Create your models here.
class WikiPage(models.Model):
    """A wiki page"""
    title = models.CharField(blank=False, max_length=100, unique=True)
    name = models.SlugField(unique=True, help_text="A short, unique name: no spaces!")
    body = models.TextField(blank=True)

    def __unicode__(self):
        return u"%s" % self.name
    
    def tangle_initialize(self):
        return "console.log('initialize', '%s')" % self
        
    def tangle_update(self):
        return "console.log('update', '%s')" % self

class WikiLink(models.Model):
    """A Link on a wiki page, extracted on save"""
    source = models.ForeignKey("WikiPage", related_name="links")
    target = models.ForeignKey("WikiPage", related_name="in_links")
    
    def __unicode__(self):
        return u'%s:%s' % (self.source.name, self.target.name)