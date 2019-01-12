from django import forms
from adminmanager.models import AdminUsers

class SearchForm(forms.Form):
    dis_roles=AdminUsers.objects.values('id','name').distinct()
    users_choice=[(r['id'],r['name'].upper()) for r in dis_roles]
    name=forms.CharField(label='Name',max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    address=forms.CharField(label='Address',widget=forms.TextInput(attrs={'class':'form-control'}))
    start_date=forms.CharField(label='Order Start',widget=forms.DateInput(attrs={'class':'form-control'},format='Y-m-d'))
    end_date=forms.CharField(label='Order End',widget=forms.DateInput(attrs={'class':'form-control'},format='Y-m-d'))
    payment_date=forms.CharField(label='Payment Date',widget=forms.DateInput(attrs={'class':'form-control'},format='Y-m-d'))
    order_by=forms.ChoiceField(label='Completed By',choices=users_choice,widget=forms.Select(attrs={'class':'form-control'}))
    is_paid=forms.ChoiceField(label='Payment',choices=(("","Any"),(1,"Completed"),(0,"Pending")),widget=forms.Select(attrs={'class':'form-control'}))
    status=forms.ChoiceField(label='Status',choices=(("","Any"),(1,"Completed"),(0,"Pending")),widget=forms.Select(attrs={'class':'form-control'}))