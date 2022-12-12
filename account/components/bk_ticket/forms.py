from django import forms


class AuthenticationForm(forms.Form):
    # bk_ticket 格式：qElJ-MDtehCC55hlP-GpWYk4ujd2eka0BtwANDdW9Qg
    bk_ticket = forms.CharField()
