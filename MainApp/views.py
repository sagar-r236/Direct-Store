from django.shortcuts import render, redirect

# Create your views here.

from . import models
from django.http import HttpResponse
import random
import os
from twilio.rest import Client





def index(request):
   
    return render(request, 'index/index.html')


def sign_up(request):
    
    if request.method == 'POST':
        #User(first_name = "Sagar", last_name = "R", mobile_number = "8431416960", user_pincode = "560091")
        otp = random.randint(1001,9999)


        #using twillio to send otp to the customer
        account_sid = "AC53325f36cc1159ce8d450786f20300d4"
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        body=f"Your Direct store OTP is {otp}", from_="+18585332596", to="+91" + request.POST['phone_number']) #end of twillio services

        user_obj = models.User(first_name = request.POST['first_name'], last_name = request.POST['last_name'], 
        mobile_number = request.POST['phone_number'], user_pincode = request.POST['pin_code'], otp = otp)
        user_obj.save()


        return render(request, 'otp_validation.html', context={'phone_number' : request.POST['phone_number']})
    return render(request, 'sign_up.html')


def otp_validator(request):
    
    if request.method == 'POST':
       try:
        user =  models.User.objects.filter(mobile_number = request.POST['phone_number'])[0]
        if user:
            print(user.otp, request.POST['otp'])
            print(type(user.otp), type(request.POST['otp']))
            
            if str(user.otp) == str(request.POST['otp']):
                
                return redirect(index)
            else:
                user.delete()
                return redirect(sign_up)
            
            
       except:
            return render(request, 'sign_up.html', context={'data': 'please entet a valid phone number'})

    return sign_up(request)



def login(request):

    if request.method == 'POST':
        try:
            user =  models.User.objects.filter(mobile_number = request.POST['phone_number'])[0]
            if user:
                
                if str(user.password) == request.POST['password']:
                    return redirect(index)
                else:
                    return render(request, 'login.html', context={'data':'password is wrong'})
            else:
                return render(request, 'login.html', context={'data':'no user found please sign up'})

        except:
            return render(request, 'login.html', context={'data':'no user found please sign up'})
            

    return render(request,'login.html')