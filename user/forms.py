from dataclasses import field
from django import forms
from .models import Account,Address
from item.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [ 'image', 'review',]

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['review'].widget.attrs.update({'class': 'form-control'})

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
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords does not match!!"
            )

        if len(password)<8:
            raise forms.ValidationError(
                "Password should contain minimum 8 characters!"
            )   

        phone_number = cleaned_data.get('phone_number')
        if len(phone_number) != 10:
            raise forms.ValidationError(
                "Enter a valid Phone number"
            )               

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=8, required=True, help_text='')

    

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pincode']


class EditUserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username',]

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})