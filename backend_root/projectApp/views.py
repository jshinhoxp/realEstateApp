# NOTE: Houses most of the algorithm in background
#NOTE: View Function always returns a HTTPResponse

import os

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from joblib import dump, load # for ML model
import pandas as pd
from geopy.geocoders import Nominatim
# Create geolocator
geoLoc = Nominatim(user_agent="myGeoloc")

from .forms import HouseForm

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import House
from projectApp.serializers import HousingSerializer

import folium
import folium.plugins

# Get the base directory of your Django project (where your manage.py file is located)
base_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
relative_path = 'projectApp\\algo\\basic_model.joblib'
file_path = os.path.join(base_dir, relative_path)

# Home Index Page
def index(request):
   # Initially create estimated price variable
   result = 0
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

   # Folium Map (starting in UW Seattle)
   m = folium.Map(location=[47.654519,-122.306732],zoom_start=12)

   # Query for all objects from database model
   house = House.objects.all()
   # converts the query to serializer
   serializer = HousingSerializer(house, many=True)
   # Gets the geographic lat and long of each address
   for dataEntry in serializer.data:
      fullAddress = str(dataEntry['address'] + ", "
         + dataEntry['city'] + ", "
         + dataEntry['state'])
      getLoc = geoLoc.geocode(fullAddress)
      print(f"Latitude: {getLoc.latitude} Longitude: {getLoc.longitude}")
      folium.Marker(
         location=[getLoc.latitude, getLoc.longitude],
         popup=fullAddress
         # NOTE: NEED TO ADD ESTIMATED PRICE in popup
      ).add_to(m)

   # Create dictionary to pass into render below
   context = {
      'myform': form,
      'result': result,
      'map': m._repr_html_, # converts follium map to html
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

# GET method
@api_view(['POST'])
def locator(request):
   # querys all data from database
   queryset= House.objects.all()
   # Convert to list
   records = list(queryset.values())
   # Covert to pandas Dataframe
   df = pd.DataFrame(records)
   print(df)
   return Response(records)


   
