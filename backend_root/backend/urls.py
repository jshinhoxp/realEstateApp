"""backend URL Configuration
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projectApp.urls')), 
    # NOTE: include takes the full Python import path to another URLconf module that should be “included” in this place.
]
