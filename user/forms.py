from dataclasses import field
from django import forms
from .models import Account,Address

class RegistrationForm(forms.ModelForm):
    # phone = forms.CharField(max_length=20, required=True, help_text='Phone_number')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Enter Password',        
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder' : 'Confirm Password'
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Firstname'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Lastname'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter Firstname'

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'input-100'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "passwords does not match!!"
            )

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='Enter code')

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pincode']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username',]