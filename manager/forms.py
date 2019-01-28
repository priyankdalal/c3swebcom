from django import forms

class LoginForm(forms.Form):
    name=forms.CharField(label="Username",required=True,widget=forms.TextInput(attrs={"placeholder":"Username"}))
    password=forms.CharField(label="Password",required=True,widget=forms.PasswordInput(attrs={"placeholder":"Password"}))

class UserSearch(forms.Form):
    name=forms.CharField(label="Name",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    address=forms.CharField(label="Address",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    expiry=forms.CharField(label="Expiry Date",required=False,widget=forms.DateInput(attrs={'class':'form-control'},format='Y-m-d'))
    pacakge=forms.CharField(label="Package",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    phone=forms.CharField(label="Phone",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    mobile=forms.CharField(label="Mobile",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    domain=forms.CharField(label="Domain",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
    ip=forms.GenericIPAddressField(label="IP",required=False,widget=forms.TextInput(attrs={'class':'form-control'}))
