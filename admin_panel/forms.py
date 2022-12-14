from cProfile import label
from dataclasses import fields
from email.mime import multipart
from pyexpat import model
from turtle import title
from django import forms
from django.forms import ChoiceField, HiddenInput, ImageField, ModelChoiceField, SelectMultiple
from property.models import PropertyFor, PropertyType, Property, Features, Country, State, City


class PropertyTypeForm(forms.ModelForm):
    class Meta:
        model = PropertyType
        fields = ['property_type_name','description','property_type_image',]

        widgets = {
            'property_type_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
            'description':forms.Textarea(attrs={'class':'form-control','placeholder':'Description'}),
            'property_type_image':forms.FileInput(attrs={'style':'margin-top:30px; margin-bottom:40px;'}),

        }

class PropertyForForm(forms.ModelForm):
    class Meta:
        model = PropertyFor
        fields = ['property_for_name']

        widgets = {
            'property_for_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
        }



class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ['country_name']

        widgets = {
            'country_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}),
        }

class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = ['state_name','country_id']

        widgets = {
            'state_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}),
            'country_id':forms.Select(attrs={'class':'form-control'})
        }

class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['city_name', 'state_id']

        widgets = {
            'city_name':forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name'}),
            'state_id':forms.Select(attrs={'class':'form-control'})
        }

# class PropertyForm(forms.ModelForm):
#     class Meta:
#         model = Property
#         fields = '__all__'

class FeaturesForm(forms.ModelForm):
    
    

    class Meta:
        model = Features
        fields = '__all__'
        exclude = ('property_id',)
        
        

        
