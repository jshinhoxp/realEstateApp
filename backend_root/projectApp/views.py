from django.shortcuts import render
from django.http import HttpResponse
# Houses most of the algorithm in background

# class ApprovalsView(viewsets.ModelViewSet):
#    # grabs anything in models    
#    queryset = Approval.objects.all()
#    serializer_class = ApprovalSerializers

def index(request):
   return HttpResponse('<h1> Django Include URLs </h1>')

def about(request):
   return HttpResponse('<h1>this is about</h1>')
