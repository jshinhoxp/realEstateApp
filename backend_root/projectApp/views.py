# NOTE: Houses most of the algorithm in background
# NOTE: View Function always returns a HTTPResponse
 
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
# Create geolocator
from geopy.geocoders import Nominatim # Uses Leaflet via geopy
geoLoc = Nominatim(user_agent="myGeoloc")
from .forms import HouseForm
# Importing the Django rest_framework for api endpoints
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Import internal model and serilizer objects
from .models import House
from projectApp.serializers import HousingSerializer
# Maps
import folium
import folium.plugins
# IPython Widgets
from ipywidgets import IntSlider 
from ipywidgets.embed import embed_minimal_html
from IPython.display import display_html
# Import python functions for creating and loading ML models
from joblib import dump, load # for ML model

import os
# Get the base directory of your Django project (where your manage.py file is located)
base_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
relative_path = 'projectApp\\ml_models\\'
file_path = os.path.join(base_dir, relative_path)

# Folium Map (starting in UW Seattle)
m = folium.Map(location=[47.654519,-122.306732],zoom_start=12)

## FUNCTIONS ##
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
      # Populate info for last entry
      entry = House.objects.latest('id') # Retrieve last entry
      fullAddress = str(entry.address + ", " +
                        entry.city + ", " +
                        entry.state)
      location = geoLoc.geocode(fullAddress)
      entry.fullAddress = fullAddress
      entry.latitude = location.latitude
      entry.longitude = location.longitude
      # Calculate the estimated price using the ML_Model
      price = algo(entry) # passes the latest django model object
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

   # Show Chart of ML Model
   zipcode_widget = chart()
   # Get the HTML representation of the widget
   html = embed_minimal_html('export.html', views=[zipcode_widget], title='Widgets Export')
   print(chart())
   print(html)

   # Create dictionary to pass into render below
   context = {
      'myform': form,
      'price': price,
      'map': m._repr_html_, # converts follium map to html
      'zipcode_widget': html
   }
   return render(request, "index.html", context)

# Receives the entry and predicts outcome using respective Zipcode model
def algo(entry):
   # Create dataframe from entry
   entryDict = {
      'bedrooms': entry.bedrooms,
      'bathrooms': entry.bathrooms,
      'sqft_living': entry.sqft_living,
      'sqft_lot': entry.sqft_lot,
      'floors': entry.floors
   }
   # Convert to dataframe
   df = pd.DataFrame([entryDict])
   # Load the condensed model file
   mdl = load(file_path + str(entry.zipcode))
   # Predict based on input
   y_pred = mdl.predict(df)
   # Return prediction
   return y_pred

# Creates and returns the machine learning chart
def chart():
   # Querys all data from database
   house = House.objects.all()
   # Serializer
   serializer = HousingSerializer(house, many=True)
   # Get all zipcodes
   df =pd.DataFrame.from_dict(serializer.data)
   # Zipcode widget
   # zipcode_widget = widgets.Select(
   #    # List the options 
   #    options=df['zipcode'].unique(),
   #    description='Zipcodes: ',
   #    disabled=False
   # )

   slider = IntSlider(value=40)
   embed_minimal_html('export.html', views=[slider], title='Widgets export')
   return slider

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


   
