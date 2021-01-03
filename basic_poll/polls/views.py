from django.shortcuts import render
from django.http import HttpResponse

import datetime

# Create your views here.

def super_basic_index(request):
    return HttpResponse("<h1>Hello</h1> You're at the polls index. <p>" + str(datetime.datetime.now()) +"</p>")

