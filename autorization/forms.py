from django import forms
from django.contrib.auth import authenticate

class PhoneAuthForm(forms.Form):
    phone_number = forms.CharField(max_length=15)
    code = forms.CharField(max_length=4)

    def clean(self):
        cleaned_data = super().clean()
        phone_number = cleaned_data.get("phone_number")
        code = cleaned_data.get("code")

        user = authenticate(phone_number=phone_number, code=code)
        if user is None:
            raise forms.ValidationError("Неверный номер телефона или код.")
        cleaned_data['user'] = user
        return cleaned_data
