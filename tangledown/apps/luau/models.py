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