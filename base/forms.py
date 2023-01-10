from django.contrib.auth.forms import UserCreationForm
from .models import Account
from allauth.account.forms import SignupForm
from django import forms
from django.forms import ModelForm
from property.models import Features

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['full_name','email']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email','full_name','phone_number','city']
   
        widgets = { 'user_type' : forms.Select(attrs={'disabled': 'disabled'}), 
                    
                        } 
                    
    def __init__(self, *args, **kwargs):
            super(UserProfileForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'
        
 
class CustomSignupForm(SignupForm):
    full_name = forms.CharField(max_length=30, label='Full Name',widget= forms.TextInput
                           (attrs={'placeholder':'Full name'}))
 
    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.full_name = self.cleaned_data['full_name']
        user.save()
        return user

class FeaturesForm(forms.ModelForm):
    class Meta:
        model = Features
        fields = '__all__'
        exclude = ('property_id',)