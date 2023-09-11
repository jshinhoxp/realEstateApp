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

# Folium Map (starting in UW Seattle)
m = folium.Map(location=[47.654519,-122.306732],zoom_start=12)

# Home Index Page
def index(request):
   # Initially create estimated price variable
   price = 0
   # Create a form object from POST data
   form = HouseForm(request.POST) 
   # Check if form data is valid
   if form.is_valid():
      # Save the form data to model via INSERT SQL
      form.save() 
      # Convert to JSON dictioanry for display
      data = form.cleaned_data   
      # Omit the specific columns
      omitted_keys = ['address', 'city', 'state']
      # loop through to omit the unwanted columns
      result_dict = {key: value for key, value in data.items() if key not in omitted_keys}
      # Convert to dataframe
      df = pd.DataFrame([result_dict])
      print(df) # Check to see if printed in terminal
      price = algo(df)
      # Populate info for last entry
      entry = House.objects.latest('id') # Retrieve last entry
      fullAddress = str(entry.address + ", " +
                        entry.city + ", " +
                        entry.state)
      location = geoLoc.geocode(fullAddress)
      entry.fullAddress = fullAddress
      entry.latitude = location.latitude
      entry.longitude = location.longitude
      entry.estPrice = price
      entry.save() # save changed entry to database
     
      # Add Marker for each dataset
      folium.Marker(
         location=[entry.latitude, entry.longitude],
         popup= folium.Popup(
            str(entry.fullAddress) + "\n $" + str(entry.estPrice), max_width=200)  
         # NOTE: NEED TO ADD ESTIMATED PRICE in popup
      ).add_to(m)

      # Go to location in map
      m.fit_bounds([(entry.latitude,entry.longitude)])

   # Create dictionary to pass into render below
   context = {
      'myform': form,
      'price': price,
      'map': m._repr_html_ # converts follium map to html
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


   
