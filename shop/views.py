from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from . import models
from random import random
import os
from twilio.rest import Client
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings




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
            return redirect('login')

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
                    request.session['user'] = mobile_number
                    print(request.session['user'])
                    return redirect('/vendor')

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



def vendor_home(request):

    
    try:
        shop_obj = models.Vendor.objects.get(mobile_number = request.session['user'])
        res = f"Hi welcome to DirectStore {shop_obj.shop_name}"
    except:
        return HttpResponse('Please Login')
    return render(request, 'index.html', context={'greet': res})



def vendor_products(request):
    
    shop = request.session['user']
    products = models.Product.objects.filter(shop__mobile_number = shop)
    print("this is", settings.MEDIA_URL)
    media_url = settings.MEDIA_URL

    return render(request, 'vendor_product.html', context={'products' : products, 'media_url': media_url})


def add_product(request):


    if request.method == 'POST':
        product_name = request.POST['product_name']
        product_price = request.POST['product_price']
        
        product_category = models.ProductCategory.objects.get(category = request.POST['product_category'] )
        product_details = request.POST['product_detail']
        product_image = request.FILES.get('product_image')
        shop_obj = models.Vendor.objects.get(mobile_number = request.session['user'])

        #creation of the product object
        product_obj = models.Product(product_name = product_name, product_price = product_price, product_category = product_category, product_details = product_details, product_image = product_image, shop = shop_obj)
        product_obj.save()
        messages.info(request, 'Product uploaded successfully')
        return redirect('add_product')

    categories = models.ProductCategory.objects.all()
    print(categories)

    return render(request, 'add_product.html', context={ 'categories' : categories })


def edit_product(request, product):

    if request.method == 'POST':
        product = models.Product.objects.get(product_name = product)
        product.product_name = request.POST['product_name']
        product.product_price = request.POST['product_price']
        product.product_category = models.ProductCategory.objects.get(category = request.POST['product_category'] )
        product.product_details = request.POST['product_detail']
        if request.FILES.get('product_image') != None:
            product.product_image = request.FILES.get('product_image')
            product.save()
            messages.info(request, 'Product Updated Successfully!')
            return redirect('/vendor/edit_product' + '/' +product.product_name)

        print(request.FILES.get('product_image'))
        product.save()
        messages.info(request, 'Product Updated Successfully!')
        return redirect('/vendor/edit_product' + '/' + product.product_name)


    product = models.Product.objects.get(product_name = product)
    print(product)
    categories = models.ProductCategory.objects.all()
    context = {
        'product' : product,
        'categories' : categories
    }
    return render(request, 'edit_product.html', context=context)



def log_out(request):

    request.session['user'] = ''
    return redirect('/')



