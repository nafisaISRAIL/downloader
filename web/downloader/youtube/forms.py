from django import forms
import re


class DownloadForm(forms.Form):
    email = forms.EmailField()
    url = forms.CharField(max_length=300)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            raise forms.ValidationError('Invalid email')

        return email
