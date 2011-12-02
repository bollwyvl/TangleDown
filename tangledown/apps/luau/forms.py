from django import forms 

from luau.models import WikiPage

class WikiPageForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 15, 
        'style': 'width:100%;'}))
    
    class Meta:
        model = WikiPage