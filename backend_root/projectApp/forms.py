from django import forms
from .models import House
from django.utils.html import escape

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
      super().__init__(*args, **kwargs) # super is class HouseForm
      for field in self.Meta.required:
         self.fields[field].required = False
   
   # Prevent cross site scripts
   def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        for field_name, field_value in list(cleaned_data.items()):
            if isinstance(field_value, str):
                # Perform additional validation here, e.g., checking for HTML tags
                if '<' in field_value or '>' in field_value:
                    self.add_error(field_name, 'Input contains invalid characters.')
                # Escape the field value to prevent XSS
                cleaned_data[field_name] = escape(field_value)
