from django.shortcuts import render, redirect

# Create your views here.

from . import models
from django.http import HttpResponse
import random
import os
from twilio.rest import Client





def index(request):
   
    return render(request, 'index/index.html')


