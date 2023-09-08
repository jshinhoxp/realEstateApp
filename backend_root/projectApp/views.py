# NOTE: Houses most of the algorithm in background
#NOTE: View Function always returns a HTTPResponse

import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from joblib import dump, load # for ML model

# Get the base directory of your Django project (where your manage.py file is located)
base_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))

# Define the relative path to your 'basic_model.joblib' file from the project root
relative_path = 'projectApp\\algo\\basic_model.joblib'

# Construct the absolute file path
file_path = os.path.join(base_dir, relative_path)

import pandas as pd
from .forms import HouseForm

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import House
from projectApp.serializers import HousingSerializer

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = House.objects.all()
    serializer_class = HousingSerializer

# Home Page
def index(request):
   # Create an object of form and posts it
   form = HouseForm(request.POST or None) 
   # Check if form data is valid
   if form.is_valid():
      # Save the form data to model
      form.save()
      # Convert to JSON dictioanry for display
      data = form.cleaned_data   
      print(data) # prints to command prompt
      # Omit the specific columns
      omitted_keys = ['address', 'city', 'state']
      # loop through to omit the unwanted columns
      result_dict = {key: value for key, value in data.items() if key not in omitted_keys}
      # Convert to dataframe
      df = pd.DataFrame([result_dict])
      print(df) # Check to see if printed in terminal
      result = algo(df)

   # Create dictionary to pass into render below
   context = {
      'myform': form,
      'result': result
   }

   return render(request, "index.html", context)

# GET method
@api_view(['GET'])
def getData(request):
   # querys all data from database
   house = House.objects.all() 
   # converts the query to serializer
   serializer = HousingSerializer(house, many=True)  
   return Response(serializer.data)

# POST method (another way of post into database)
@api_view(['POST'])
def addData(request):
   serializer = HousingSerializer(data=request.data)
   if serializer.is_valid():
      serializer.save()
      
   return Response(serializer.data)


# Receives the input dataframe and predicts the model
def algo(df):
   # Load the condensed model file
   mdl = load(file_path)
   # Predict based on input
   y_pred = mdl.predict(df)
   # Return result
   return y_pred


   
