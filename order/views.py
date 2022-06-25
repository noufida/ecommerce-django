from calendar import month
from user.models import Address
from django.shortcuts import render,redirect
from cart.models import CartItem
from item.models import Item
from .models import Order,Payment,OrderProduct
import datetime
import razorpay
from django.contrib import messages
from cart.models import Discount
from categories.models import Category,SubCategory



from django.template.loader import render_to_string
from django.core.mail import EmailMessage

import json
import urllib

from django.conf import settings

# Create your views here.

def place_order(request, total=0, quantity=0):
    women = SubCategory.objects.filter(gender__startswith = 'W')
    men = SubCategory.objects.filter(gender__startswith = 'M')    
    category = Category.objects.all()

    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)    

    if cart_item :
       
        print('hdsf')  
        tax = 0
        grand_total = 0
        discount=0
        grand_total_without=0
        for item in cart_item:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = (2*total)/100
        grand_total_without = total + tax
        print(grand_total_without)
        try:
            discounted = Discount.objects.get(user=request.user)
            print(discounted)
            discount = discounted.discount_appleid
            print(discount)
            grand_total = grand_total_without-(discount*grand_total_without)
        except:
           
            discounted = Discount.objects.filter(user=request.user)           
            grand_total = total + tax

        if request.method == 'POST': 
            
            if 'address' in request.POST:
                print("adres")
                address = request.POST['address']  
                curr_address = Address.objects.get(id=address)  
                                    
                data = Order()
                data.user = current_user
                data.address = curr_address
                data.order_total = grand_total
                data.tax = tax
                data.ip=request.META.get('REMOTE_ADDR')
                data.save()

                #generate order number
                yr= int(datetime.date.today().strftime('%Y'))
                dt= int(datetime.date.today().strftime('%d'))
                mt= int(datetime.date.today().strftime('%m'))
                d=datetime.date(yr,mt,dt)
                current_date =d.strftime("%Y%m%d")
                
                order_number=current_date +str(data.id)
                print(order_number)
                data.order_number = order_number
                data.save()

                request.session['order_number'] = order_number
                
                context={
                    'add' : curr_address,
                    'cart_items' : cart_item,
                    'tax' : tax,
                    'grand_total' : grand_total,
                    'grand_total_without' : grand_total_without,
                    'discount' : discount,

                    'men' : men,
                    'women' : women,
                    'category' : category,
                }
                
                return render(request, 'order/payement.html',context)

            else:
                messages.error(request, 'Address is required')
                return redirect('checkout')
            
    else:
       
        return redirect('shop')


def payment(request):
    women = SubCategory.objects.filter(gender__startswith = 'W')
    men = SubCategory.objects.filter(gender__startswith = 'M')    
    category = Category.objects.all()

    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)
    if cart_item :
        total=0
        quantity=0
        tax = 0
        grand_total = 0
        discounted=0
        for item in cart_item:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = (2*total)/100
        grand_total_without = int(total + tax)*100
        
        try:
            discounted = Discount.objects.get(user=request.user)
            print(discounted)
            discount = discounted.discount_appleid
            print(discount)
            grand_total = int(grand_total_without-(discount*grand_total_without))
            Discount.objects.get(user=request.user).delete()
        except:          
            
            grand_total = int(total + tax)*100         
        display = grand_total/100

    # creating razorpay client
    client =  razorpay.Client(auth=(settings.RAZORPAY_ID , settings.RAZORPAY_KEY ))
    
    #create order
    response_payment = client.order.create(dict(amount = grand_total, currency = 'INR'))
    print(response_payment)
    order_id = response_payment['id']
    order_status = response_payment['status']

    if order_status == 'created':       
        paym = Payment()     
        paym.user=current_user
        print(paym.user)       
        paym.amount_paid = grand_total
        paym.order_id = order_id
        paym.save()
        user = Payment.objects.get(user=current_user,order_id=order_id)

    context ={
        'user':user,
        'paym' : response_payment,
        'cart_items' : cart_item, 
        'tax' : tax,
        'grand_total' : grand_total,
        'total' : total,
       'display':display,

       'men' : men,
       'women' : women,
       'category' : category,
    }
    return render(request, 'order/razor.html',context)


def payment_status(request):
    response = request.POST
    params_dict = {
        'razorpay_order_id' : response['razorpay_order_id'],
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_signature' : response['razorpay_signature'],
    }

    #create client instance
    client = razorpay.Client(auth=(settings.RAZORPAY_ID , settings.RAZORPAY_KEY ))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id = response['razorpay_payment_id']
        payment.paid = True
        payment.save()
        print("a")
        order_number = request.session['order_number']
        print(order_number)        
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
        order.is_ordered = True
        order.status = 'Confirmed'
        order.save()
        cart_items = CartItem.objects.filter(user = request.user)
      
        for x in cart_items:
        
            data = OrderProduct()
            data.order_id = order.id            
            data.user_id = request.user.id
            data.product_id = x.product_id
            data.quantity = x.quantity
            data.payement = payment          
            data.product_price = x.product.price
            data.ordered = True
         
            # if x.variations:                
            #     data.variation = var
            data.save()
           

            pr = x.product
            product = Item.objects.get(id=pr.id)
            product.stock -= x.quantity
            product.save()
           

        cart_items.delete()     
  

        mail_subject = 'THANKYOU FOR SHOPPING WITH US'
        message = render_to_string('user/sucess.html',{
                'user' : request.user,
                
            })
        to_email = request.user.email
        send_email = EmailMessage(mail_subject, message, to=[to_email])
        send_email.send()

        return render(request, 'order/payment_status.html', {'status':True,} )
    except:
        print("except")
        payment = Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id = response['razorpay_payment_id']
        payment.paid = False
        payment.save()
        print("a")
        order_number = request.session['order_number']
        print(order_number)
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
        order.is_ordered = False
        order.status = 'Failed'
        order.save()
        cart_items = CartItem.objects.filter(user = request.user)
    
        for x in cart_items:
        
            data = OrderProduct()
            data.order_id = order.id            
            data.user_id = request.user.id
            data.product_id = x.product_id
            data.quantity = x.quantity
            data.payement = payment          
            data.product_price = x.product.price
            data.ordered = False
         
            # if x.variations:                
            #     data.variation = var
            data.save()
        return render(request, 'order/payment_status.html', {'status':False,})




def cod(request):
    women = SubCategory.objects.filter(gender__startswith = 'W')
    men = SubCategory.objects.filter(gender__startswith = 'M')    
    category = Category.objects.all()

    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)
    if cart_item :
        total=0
        quantity=0
        tax = 0
        grand_total = 0
        discounted=0
        for item in cart_item:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = (2*total)/100
        grand_total_without = int(total + tax)*100
        
        try:
            discounted = Discount.objects.get(user=request.user)
            print(discounted)
            discount = discounted.discount_appleid
            print(discount)
            grand_total = int(grand_total_without-(discount*grand_total_without))
            Discount.objects.get(user=request.user).delete()
        except:          
            
            grand_total = int(total + tax)*100         
        display = grand_total/100 

    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())

        if result['success']:
            messages.success(request, 'Your Order Placed Successfully!!')
            order_number = request.session['order_number']
            print(order_number)
            order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
            order.is_ordered = True
            order.status = 'Confirmed'
            order.save()
            cart_items = CartItem.objects.filter(user = request.user)
        
            for x in cart_items:
            
                data = OrderProduct()
                data.order_id = order.id            
                data.user_id = request.user.id
                data.product_id = x.product_id
                data.quantity = x.quantity                      
                data.product_price = x.product.price
                data.ordered = True
            
                # if x.variations:                
                #     data.variation = var
                data.save()
            

                pr = x.product
                product = Item.objects.get(id=pr.id)
                product.stock -= x.quantity
                product.save()
            

            cart_items.delete()     
    

            mail_subject = 'THANKYOU FOR SHOPPING WITH US'
            message = render_to_string('user/sucess.html',{
                    'user' : request.user,
                    
                })
            to_email = request.user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

        else:
            messages.error(request, 'Invalid reCAPTCHA, Please try again!!')
    context ={
        
            'cart_items' : cart_item, 
            'tax' : tax,
            'grand_total' : grand_total,
            'total' : total,
            'display':display,

            'women' : women,
            'men' : men,
            'category' : category,
        }

    return render(request, 'order/cod.html',context)