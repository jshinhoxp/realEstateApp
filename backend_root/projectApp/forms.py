from django import forms
from .models import House

class HouseForm(forms.ModelForm):   
   
   class Meta:
      n = {'address', 'city', 'state', 'zipcode', 'bedrooms', 'bathrooms',
         'sqft_living','sqft_lot','floors'}
      model = House
      fields = n
      required = {'address', 'city', 'state', 'bedrooms', 'bathrooms', 'sqft_living','sqft_lot','floors'}

   field_order = ['address', 'city', 'state', 'zipcode', 'bedrooms',
         'bathrooms', 'sqft_living', 'sqft_lot', 'floors']
   
   def __init__(self, *args, **kwargs):
      # First call parent constructor
      super().__init__(*args, **kwargs)

      for field in self.Meta.required:
         self.fields[field].required = False

class myForm(forms.Form):
    name = forms.CharField(label="Name", max_length=200, required=False)