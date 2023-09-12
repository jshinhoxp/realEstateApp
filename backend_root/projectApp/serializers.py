# Mechanism that handles request and converts to json file

from rest_framework import serializers
from .models import House

# Serializers define the API representation.
class HousingSerializer(serializers.ModelSerializer):
   class Meta:
      model=House
      fields='__all__'