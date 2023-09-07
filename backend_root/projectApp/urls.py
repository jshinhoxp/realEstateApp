from . import views
from django.urls import path, include
from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('projectApp', views.ApprovalsView)
urlpatterns = [
    path('', views.index, name = 'home'),
    # path('about/', views.about, name = 'about')
    # path('api/', include(router.urls)),
    # path('status/', views.approvereject),
]
