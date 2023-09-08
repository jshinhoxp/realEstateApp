# NOTE: Houses most of the algorithm in background
#NOTE: View Function always returns a HTTPResponse

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from joblib import dump, load # for ML model
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
      # Redirect to admin page
      return HttpResponseRedirect("admin/")
   
   # Create dictionary to pass into render below
   context = {
      'myform': form
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