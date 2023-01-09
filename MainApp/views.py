from django.shortcuts import render, redirect

# Create your views here.


from django.http import HttpResponse
from random import random
import os
from twilio.rest import Client
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect


from .models import *
from shop.models import *

def index(request):
   
    return render(request, 'index/index.html')


def sign_up(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']
        
        pincode = request.POST['pincode']
        
        user_obj = models.User.objects.filter(mobile_number = mobile_number)
        print(user_obj)

        if user_obj.exists():
            messages.info(request, "Your account already exists please login")
            return redirect('login_user')
        
        else:   #create user object if the user is not found

            #creating shop object if the vendor is not found
            otp = int((random() * 10000))

            #using twilio to send otp
            account_sid = "AC53325f36cc1159ce8d450786f20300d4"
            auth_token = os.environ["TWILIO_AUTH_TOKEN"]
            client = Client(account_sid, auth_token)
            message = client.messages.create(
            body=f"Your Direct store OTP is {otp}", from_="+18585332596", to="+91" + request.POST['mobile_number'])
            #end of twilio block

            #user object is created and saved

            user_obj = models.User(first_name = first_name, mobile_number = mobile_number, password = password, user_pincode = pincode, otp = otp)
            
            user_obj.save()
            
            messages.info(request, "Please login with the otp sent to your phone number")
            return redirect('login_user')





    return render(request, 'users/sign_up.html' )



def login(request):

    if request.method == 'POST':
        
        mobile_number = request.POST['mobile_number']
        password = request.POST['password']


        # try:
        user_obj = User.objects.get(mobile_number = mobile_number)
        # except:
        #     return HttpResponse("User doesn't exist")
        
        # print(user_obj)
        
        if user_obj:
            if (user_obj.password == password):
                request.session['user'] = user_obj.mobile_number
                return redirect('user_index')
        else:
            return HttpResponse("password is wrong")
        return render(request, 'users/login.html')

    return render(request, 'users/login.html')


def user_index(request):
    
    request.session['vendor'] = None

    user_obj = User.objects.get(mobile_number = request.session['user'])
    shop_qs = Vendor.objects.filter(pincode = user_obj.user_pincode)
    
    

    return render(request, 'users/index.html', context={'shops' : shop_qs})


def explore_shop(request, vendor_number):
    
    shop = Vendor.objects.get(mobile_number = vendor_number)
    shop_products = Product.objects.filter(shop = shop)
    print(shop_products)

    context = {
        'shop_products' : shop_products
    }

    request.session['vendor'] = vendor_number
    print(request.session['vendor'])
    return render(request, 'users/shop_explore.html', context=context)


def add_to_cart(request, product):
    
    user_obj = User.objects.get(mobile_number = request.session['user'])
    print(user_obj)
    product_obj = Product.objects.get(product_name = product)


    #checking if the item is already present in the cart
    items = Cart.objects.filter(user = user_obj, product = product_obj)

    if items.exists():
        messages.info(request, "Item already in the cart")
        url = reverse('explore_shop', args=[request.session['vendor']])
        return redirect(url)
    
    
    cart = Cart(user = user_obj, product = product_obj)
    cart.save()

    messages.info(request, "Sucessfully added to cart ")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart(request):
    
    user_obj = User.objects.get(mobile_number = request.session['user'])
    cart = Cart.objects.filter(user = user_obj)
    print(cart)

    return render(request, 'users/cart.html', context={'cart' : cart})


def remove_item(request, product):
    
    user_obj = User.objects.get(mobile_number = request.session['user'])
    item = Cart.objects.get(user = user_obj, product= product)
    item.delete()

    messages.info(request, "Item removed Successfully")
    return redirect('cart')


