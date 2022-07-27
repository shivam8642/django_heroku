from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from .models import Address,City

class Signupform(UserCreationForm):
    first_name = forms.CharField(max_length=10)
    last_name = forms.CharField(max_length=10)
    email = forms.EmailField()
    password1 = forms.CharField(label='Enter password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password',widget=forms.PasswordInput)
    class Meta(UserCreationForm):
        model=User
        fields=['username','first_name','last_name','email','password1','password2']

    def clean_email(self):
      email=self.cleaned_data['email']
      if User.objects.filter(email= email).exists():
        raise forms.ValidationError("Email already exists")
      return email

class MyUserChangeForm(forms.ModelForm):
    password = None
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')
  

class AddressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=('first_name','last_name','address','country','city','pincode','mobile_no')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.none()

        if 'country' in self.data:
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')




 