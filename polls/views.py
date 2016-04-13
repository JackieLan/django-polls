from django.shortcuts import render
from django.http import HttpResponse

index_content = "Hello World!"
# Create your views here.
def index(request):
    return HttpResponse(index_content)
