from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.
def profile(request):
    return HttpResponse("Hello, " + str(__name__))