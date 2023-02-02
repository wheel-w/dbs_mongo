from django import forms


class AuthenticationForm(forms.Form):
    bk_ticket = forms.CharField()
