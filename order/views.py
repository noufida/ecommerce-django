from calendar import month
from http import client
from user.models import Address
from django.shortcuts import render,redirect
from cart.models import CartItem
from item.models import Item
from .models import Order,Payment
import datetime
from django.http import HttpResponse 
import razorpay
from django.contrib import messages


# Create your views here.

def place_order(request, total=0, quantity=0):
    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)    

    if cart_item :
       
            print('hdsf')  
            tax = 0
            grand_total = 0
            for item in cart_item:
                total += item.product.price * item.quantity
                quantity += item.quantity
            tax = (2*total)/100
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
                    
                    context={
                        'add' : curr_address,
                        'cart_items' : cart_item,
                        'tax' : tax,
                        'grand_total' : grand_total,
                        'total' : total,
                    }
                    
                    return render(request, 'order/payement.html',context)

                else:
                    messages.error(request, 'Address is required')
                    return redirect('checkout')
            
    else:
       
        return redirect('shop')


def payment(request):
    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)
    if cart_item :
        total=0
        quantity=0
        tax = 0
        grand_total = 0
        for item in cart_item:
            total += item.product.price * item.quantity
            quantity += item.quantity
        tax = (2*total)/100
        grand_total = int(total + tax)*100

    # creating razorpay client
    client =  razorpay.Client(auth=('rzp_test_efcfepUZ9n5uwO' , 'aFoMVtEn3GwEFSgsJ5PJ9Rbf' ))
    
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
    client = razorpay.Client(auth=('rzp_test_efcfepUZ9n5uwO' , 'aFoMVtEn3GwEFSgsJ5PJ9Rbf' ))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        payment = Payment.objects.get(order_id=response['razorpay_order_id'])
        payment.payment_id = response['razorpay_payment_id']
        payment.paid = True
        payment.save()
        cart_items = CartItem.objects.filter(user = request.user)
        print(cart_items)
        for x in cart_items:
            
            pr = x.product
            product = Item.objects.get(id=pr.id)
            product.stock -= x.quantity
            product.save()
        cart_items.delete()     
        return render(request, 'order/payment_status.html', {'status':True,} )
    except:
        return render(request, 'order/payment_status.html', {'status':False,})

