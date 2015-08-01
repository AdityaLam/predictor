from django import forms

class FileForm(forms.Form):
    csv = forms.FileField(label='Upload CSV')