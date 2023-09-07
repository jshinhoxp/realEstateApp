# Mechanism that handles request and converts to json file

from rest_framework import serializers
from .models import Housing

class HousingSerializers(serializers.ModelSerializer):
   class Meta:
      model=Housing
      fields='__all__'
      