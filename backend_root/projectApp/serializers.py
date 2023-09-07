# Mechanism that handles request and converts to json file

from rest_framework import serializers
from .models import Approval

class approvalsSerializers(serializers.ModelSerializer):
   class Meta:
      model=Approval
      fields='__all__'
      
