from django import forms
from django.forms.formsets import formset_factory

class PartForm(forms.Form):
    number = forms.CharField()

PartFormSet = formset_factory(PartForm, extra = 5)

class NameForm(forms.Form):
    uid = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    name = forms.CharField()
    email = forms.CharField()