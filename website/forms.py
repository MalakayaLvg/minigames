from django import forms

class PenduForm(forms.Form):
    letter = forms.CharField(max_length=1, label='letter')
    widget=forms.TextInput(attrs={"class":"form-control"})

class CemantixForm(forms.Form):
    word = forms.CharField(max_length=50,label='word')
    widget=forms.TextInput(attrs={"class":"form-control"})