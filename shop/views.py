from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from random import random
import os
from twilio.rest import Client
from django.http import HttpResponse
from django.contrib import messages






def sign_up(request):

    if request.method == 'POST':
        shop_name = request.POST['shop_name']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        pincode = request.POST['pincode']
       
        #filtering to check whether vendor already exists
        shop_obj = models.Vendor.objects.filter(mobile_number= mobile_number)
    

        if shop_obj.exists():
            messages.info(request, "Your account already exist please login")
            redirect('login')

        else:

            #creating shop object if the vendor is not found
            otp = int((random() * 10000))

            #using twilio to send otp
            account_sid = "AC53325f36cc1159ce8d450786f20300d4"
            auth_token = os.environ["TWILIO_AUTH_TOKEN"]
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body=f"Your Direct store OTP is {otp}", from_="+18585332596", to="+91" + request.POST['mobile_number'])
            #end of twilio block

            #shop objects is created and saved
            shop_obj = models.Vendor(shop_name = shop_name, mobile_number = mobile_number, password = password,pincode = pincode, otp = otp )
            shop_obj.save()

            messages.info(request, "Please login with the otp sent to your phone number")
            return redirect('login')


    

    return render(request, 'shop/signup.html')


def login(request):

    if request.method == 'POST':

            mobile_number = request.POST['mobile_number']
            password = request.POST['password']
            
            # filtering the shop objects 
            shop_obj = models.Vendor.objects.filter(mobile_number=mobile_number)

            

            #if the shop does not exists then send message and redirect to sign_up
            if not shop_obj.exists():       
                 messages.info(request, "Phone number doesn't exist please sign up")
                 return redirect('sign_up')

            
            if shop_obj[0].is_verified:
                if shop_obj[0].password == password:
                    return HttpResponse('Successfully logged in')

            #logic for if the shop exist and shop is not verified
            if shop_obj.exists():

                #logic for if the otp is sent and shop is not verified
                if (not shop_obj[0].is_verified) and (shop_obj[0].otp != None):
                    print(password, shop_obj[0].otp)
                    if (str(password) == str(shop_obj[0].otp)):
                        update_shop_obj = shop_obj[0]
                        update_shop_obj.is_verified = True
                        update_shop_obj.otp = None
                        update_shop_obj.save(update_fields=['otp', 'is_verified'])
                        return HttpResponse('successfully logged in')

                
                #logic for if the otp is not sent and shop is not verifiec
                if not shop_obj[0].is_verified:
                    print('that is being executed')
                    #creating shop object if the vendor is not found
                    otp = int((random() * 10000))

                    # #using twilio to send otp
                    account_sid = "AC53325f36cc1159ce8d450786f20300d4"
                    auth_token = os.environ["TWILIO_AUTH_TOKEN"]
                    client = Client(account_sid, auth_token)
                    message = client.messages.create(
                    body=f"Your Direct store OTP is {otp}", from_="+18585332596", to="+91" + request.POST['mobile_number'])
                    # #end of twilio block

                    #reassinging the otp
                    print(f'Reassigned otp is {otp}')
                    update_shop_obj = shop_obj[0]
                    update_shop_obj.otp = otp
                    
                    update_shop_obj.save(update_fields=['otp'])
                    messages.info(request, "Please verify the account with otp sent")
                    return redirect('login')


        
        
        

    return render(request, 'shop/login.html')