# NOTE: Houses most of the algorithm in background
# NOTE: View Function always returns a HTTPResponse

from django.shortcuts import render
import pandas as pd
from geopy.geocoders import Nominatim # Uses Leaflet via geopy
# Import internal form, model and serilizer objects
from .forms import HouseForm
from .models import House
from projectApp.serializers import HousingSerializer
# Maps
import folium
import folium.plugins
# Import python functions for creating and loading ML models
from joblib import dump, load # for ML model
# Import Model Development
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.metrics import mean_squared_error 

import plotly.express as px
import plotly.graph_objects as go

import json

import os

'''START HERE'''
# Get the base directory of your Django project (where your manage.py file is located)
base_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '..')))
# Geographic Locator Object using Leaflet Nominatim
geoLoc = Nominatim(user_agent="myGeoloc")
# Folium Map (starting in UW Seattle)
m = folium.Map(location=[47.654519,-122.306732],zoom_start=12)
# Load the house data
sales = pd.read_csv(
   os.path.join(base_dir, 'projectApp/ml_script/home_data.csv'))
# Order by zipcode
sales = sales.sort_values('zipcode')

# PAGES
# Home Index Page
def index(request):
   # Initially create estimated price variable
   price = 0
   zipcode = 98105 # Gas Works Park (initial zipcode)
   # Monitor if request was sent from user
   if request.method == "POST":
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
         zipcode = entry.zipcode 
         # Calculate the estimated price using the ML_Model
         price = calcPrice(entry) # passes the latest django model object
         entry.estPrice = price      
         entry.save() # save changed entry to database
   else:
      form = HouseForm() # blank form

   # Mark all points in database
   mapMarker()


   # Converts the plotly figures to html
   fig1_html = chart1(sales, zipcode).to_html()
   fig2_html = datasetChart(sales).to_html()

   # Create dictionary to pass into render below
   context = {
      'myform': form,
      'price': price,
      'map': m._repr_html_, # converts follium map to html
      'fig1': fig1_html,
      'fig2': fig2_html,
      'nbar': "index" # highlights active link on navbar
   }
   return render(request, "index.html", context)

def about(request):
   hello = "Hello World!"
   context = {'hello':hello,
              'nbar': "about"} # highlights active link on navbar
   return render(request, "about.html", context)

###### FUNCTIONS ######
def mapMarker():
   # querys all data from database
   queryset= House.objects.all()
   # Convert to list
   records = list(queryset.values())
   # Covert to pandas Dataframe
   df = pd.DataFrame(records)
   # Extract only latitude and longitudes
   df = df[
      ['address','city','state','zipcode', 'latitude','longitude','estPrice']]
   # Iterate through the rows of the DataFrame
   for index, row in df.iterrows():
      # Create a folium.Marker for each row
      marker = folium.Marker(
         location=[row['latitude'], row['longitude']],
         popup=folium.Popup(
            row['address'] + "<br>" + row['city'] + ", " + row['state'] + 
            ", " + str(row['zipcode']) + "<br><b>$" + str(row['estPrice']/1000) +"K</b>",
            max_width=200,
            lazy=True,
            )
      )
      # Add the markers to the map
      marker.add_to(m)
      
   # Create geojson layer for folium map
   geojson_layer = folium.GeoJson(
      os.path.join(base_dir, 'projectApp/ml_script/zipcodes.geojson'),
      name="Seattle WA Zipcodes").add_to(m)
   

   folium.LayerControl().add_to(m)



# Receives the entry and predicts outcome using respective Zipcode model
def calcPrice(entry):
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
   mdl = load(
      os.path.join(base_dir, 'projectApp/ml_models/' + str(entry.zipcode)))
   # Predict based on input
   y_pred = mdl.predict(df)
   # Return prediction
   return y_pred

def chart1(sales, zipcode):
   # Filter sales df by zipcode
   df = sales[sales['zipcode']==zipcode]
   fig2 = px.scatter(df, x="sqft_living", y="price")
   # Get the latest entry
   query= House.objects.latest('id')
   serializer = HousingSerializer(query)  

   # Add the entry point 
   fig2.add_trace(
    go.Scatter(
        x=[serializer.data["sqft_living"]],
        y=[serializer.data["estPrice"]],
        marker_symbol='x',
        marker_size=15,
        name="Estimated Price",
        showlegend=True)
   )
   # Set title
   fig2.update_layout(title_text="Price vs Sqft_living <br> Zipcode:" + 
                      str(zipcode))
   return fig2

def train_test_dict(list_of_df_train1, list_of_df_test1, zipcode):
   trainDf = list_of_df_train1['zipcode']
   testDf = list_of_df_test1['zipcode']
   

# Dataset chart
def datasetChart(sales):      
   # Shows the geographic data
   fig2= px.scatter(sales, x="long", y="lat",
                  color='zipcode', title='Seattle Metro Housing Dataset 2014',
                  size='price',
                  )
   return fig2

# Creates the Linear Regression Models for Housing Prices
def createMLmodels():
   # Order by zipcode
   sales = sales.sort_values('zipcode')
   # Create a list of the unique zipcodes (numpy.ndarray)
   unique_zipcodes = sales['zipcode'].unique()
   # Create list of dataframes by zipcode
   list_of_df = []
   list_of_df_train = []
   list_of_df_test = []

   for zipcode in unique_zipcodes:
      # Create df for each zipcode
      df = sales[sales['zipcode'] == zipcode]
      # Append to the list_of_df
      list_of_df.append(df)

   # Split each dataframe into train (80%) and test data (20%) 
   for df in list_of_df:
      train_data, test_data = train_test_split(df, test_size=0.2)
      list_of_df_train.append(train_data)
      list_of_df_test.append(test_data)
   # Use a loop to assign labels
   list_of_df_train1 = {}
   for zipcode, df in zip(unique_zipcodes, list_of_df_train):
      list_of_df_train1[zipcode] = df
   # Use a loop to assign labels
   list_of_df_test1 = {}
   for zipcode, df in zip(unique_zipcodes, list_of_df_test):
      list_of_df_test1[zipcode] = df

   # List features to use for model to predict 
   basic_features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors']

   list_of_models = []
   list_of_rmse_basic_train = []

   # Basic Model
   for df in list_of_df_train:
      y = df.price # actual price column of training set
      X = df[basic_features] # rest of dataframe data
      # Create and train the model
      basic_model = linear_model.LinearRegression().fit(X, y)
      # Store the model into list of models
      list_of_models.append(basic_model)
      # Predict prices using the model
      y = df.price # actual price column of training set
      X = df[basic_features]
      y_pred = basic_model.predict(X)
      train_rmse_basic = mean_squared_error(y, y_pred, squared=False) #False = rmse
      list_of_rmse_basic_train.append(train_rmse_basic)

   # Comparing with Test Data
   list_of_rmse_basic_test = []

   i = 0
   while i < len(list_of_models):
      df = list_of_df_test[i]
      y = df.price
      X = df[basic_features]
      y_pred = list_of_models[i].predict(X)
      test_rmse_basic = mean_squared_error(y, y_pred, squared=False) #False = rmse
      list_of_rmse_basic_test.append(test_rmse_basic)
      i += 1

   rmse_df = pd.DataFrame({
   'unique_zipcodes': unique_zipcodes,
   'list_of_rmse_basic_train': list_of_rmse_basic_train,
   'list_of_rmse_basic_test': list_of_rmse_basic_test
   })
   
   # Create and dump models into designated folder
   i = 0
   while (i < len(list_of_models)):
      model = list_of_models[i]
      zipcode = unique_zipcodes[i]
      dump(model, os.path.join(base_dir, 'projectApp/ml_models/' + str(zipcode)))
      i += 1
   
   return list_of_df_train1, list_of_df_test1, rmse_df