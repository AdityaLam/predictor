from django import forms

class FileForm(forms.Form):
    filename = forms.CharField(max_length = 50)
    csv = forms.FileField(label='Upload CSV')