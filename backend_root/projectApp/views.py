from django.shortcuts import render
from django.http import HttpResponse
from joblib import dump, load
# Houses most of the algorithm in background

# class ApprovalsView(viewsets.ModelViewSet):
#    # grabs anything in models    
#    queryset = Approval.objects.all()
#    serializer_class = ApprovalSerializers

def index(request):

   return render(request, "index.html", {})

def prediction(request):
   # Load
   sales = pd.read_csv('home_data.csv') 
   basic_features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors', 'zipcode']
   model = joblib.load("basic_model.joblib")
   y_pred = mdl.predict()
