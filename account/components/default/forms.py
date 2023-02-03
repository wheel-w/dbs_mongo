from django import forms


class AuthenticationForm(forms.Form):
    dbs_token = forms.CharField()
