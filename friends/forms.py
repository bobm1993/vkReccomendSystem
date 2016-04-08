from django import forms


class UserForm(forms.Form):
    current_id = forms.CharField(max_length=10)
