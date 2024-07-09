# forms.py
from django import forms

class FetchCallSummaryForm(forms.Form):
    call_id = forms.CharField(label='Call ID', max_length=100)
class Fetchcallanalyticsform(forms.Form):
    call_id = forms.CharField(label='Call ID', max_length=100)
class createcallform(forms.Form):
    # name=forms.CharField(label="name",max_length=20)
    # phone_number=forms.CharField(label="phone",max_length=12)
    lead=forms.CharField(label="lead")