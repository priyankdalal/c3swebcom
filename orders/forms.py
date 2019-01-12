from django import forms
from adminmanager.models import AdminUsers

class SearchForm(forms.Form):
    dis_roles=AdminUsers.objects.values('id','name').distinct()
    users_choice=[(r['id'],r['name'].upper()) for r in dis_roles]
    name=forms.CharField(label='Name',required=False,max_length=100,widget=forms.TextInput(attrs={'class':'form-control',"disabled":True}))
    address=forms.CharField(label='Address',required=False,widget=forms.TextInput(attrs={'class':'form-control',"disabled":True}))
    start_date=forms.CharField(label='Order Start',required=False,widget=forms.DateInput(attrs={'class':'form-control'},format='Y-m-d'))
    end_date=forms.CharField(label='Order End',required=False,widget=forms.DateInput(attrs={'class':'form-control'},format='Y-m-d'))
    payment_date=forms.CharField(label='Payment Date',required=False,widget=forms.DateInput(attrs={'class':'form-control',"disabled":True},format='Y-m-d'))
    order_by=forms.ChoiceField(label='Completed By',required=False,choices=users_choice,widget=forms.Select(attrs={'class':'form-control'}))
    is_paid=forms.ChoiceField(label='Payment',required=False,choices=(("","Any"),(1,"Completed"),(0,"Pending")),widget=forms.Select(attrs={'class':'form-control'}))
    status=forms.ChoiceField(label='Status',required=False,choices=(("","Any"),(1,"Completed"),(0,"Pending")),widget=forms.Select(attrs={'class':'form-control'}))