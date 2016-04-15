from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    response_content = "Hello World!"
    return HttpResponse(response_content)
