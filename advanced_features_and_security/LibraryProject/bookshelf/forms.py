from django import forms

class ExampleForm(forms.Form):
    title = forms.CharField(max_length=200, label='Book Title')
    author = forms.CharField(max_length=100, label='Author Name')
    publication_year = forms.IntegerField(label='Publication Year')
