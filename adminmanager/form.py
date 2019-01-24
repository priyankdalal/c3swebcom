from django import forms

class EditForm(forms.Form):
    id=forms.CharField(label="id",widget=forms.HiddenInput())
    name=forms.CharField(label="Name",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label="OrigPassword",required=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_string=forms.CharField(label="Password",required=False,widget=forms.PasswordInput(render_value=True,attrs={'class':'form-control'}))
    role=forms.ChoiceField(label="Role",required=False,choices=(("admin","Admin"),("operator","Operator")),widget=forms.Select(attrs={'class':'form-control'}))
    password_changed=forms.CharField(label="pass_change",widget=forms.HiddenInput(attrs={'value':'0'}))

class AddForm(forms.Form):
    name=forms.CharField(label="Name",required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label="OrigPassword",required=False,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password_string=forms.CharField(label="Password",required=True,widget=forms.PasswordInput(render_value=True,attrs={'class':'form-control'}))
    role=forms.ChoiceField(label="Role",required=True,choices=(("admin","Admin"),("operator","Operator")),widget=forms.Select(attrs={'class':'form-control'}))
