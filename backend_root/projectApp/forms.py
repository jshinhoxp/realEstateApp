from django import forms
from .models import House

class HouseForm(forms.ModelForm):
   class Meta:
      model = House
      fields = {'address',
         'city',
         'state',
         'bedrooms',
         'bathrooms',
         'sqft_living',
         'sqft_lot',
         'floors'}
   field_order = ['address',
         'city',
         'state',
         'bedrooms',
         'bathrooms',
         'sqft_living',
         'sqft_lot',
         'floors']