from django import forms


class AuthForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    type = forms.ChoiceField(widget=forms.HiddenInput(), choices=(
        ('UP', 'up'),
        ('IN', 'in'),
    ))
