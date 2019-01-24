from django import forms

class addForm(forms.Form):
    name=forms.CharField(label="Name",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    code=forms.CharField(label="Code",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))

class editForm(addForm):
    id=forms.CharField(label="id",required=True,widget=forms.HiddenInput())
