from . import views
from django.urls import path, include
from rest_framework import routers
from . import views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
# router.register('projectApp', views.ApprovalsView)

urlpatterns = [
    path('', views.index, name = 'index'), 
    path('api/', views.getData),
    path('api/add', views.addData),
    path('locator', views.locator),
    path('create',views.create, name="create")
]
