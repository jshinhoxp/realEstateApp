# NOTE: Houses most of the algorithm in background

from django.shortcuts import render
from django.http import HttpResponse
from joblib import dump, load # for ML model
from .forms import HouseForm


# Home Page
def index(request):
   # Create an object of form and posts it
   form = HouseForm(request.POST or None) 
   # Check if form data is valid
   if form.is_valid():
      # Save the form data to model
      form.save()
   # Create dictionary to pass into render below
   context = {
      'form': form
   }
   return render(request, "index.html", context)
   