from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
from item.models import Item, Wish
from item.models import Variation
from django.contrib.auth.decorators import login_required
from user.forms import AddressForm
from user.models import Address

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    current_user = request.user
    product = Item.objects.get(id=product_id) #get the product

    #when user is authenticated
    if current_user.is_authenticated:
        print("auth")
        product_variation = []
        if request.method == 'POST':
            print('plus chech chec')

            # color = request.POST['color__radio']
            # size = request.POST['size']
            for item in request.POST:
                key = item
                value = request.POST[key]        
                print(key)
                print(value)

                try:                      
                    variation = Variation.objects.get(product=product, variation_value=value, variation_category=key)
                    print(variation) 
                    product_variation.append(variation)
                except:
                    pass                       
            

        is_cart_item_exists = CartItem.objects.filter(product=product,user=current_user).exists()
        print(is_cart_item_exists)
        if is_cart_item_exists:
            print("cart alreay")          
            cart_item = CartItem.objects.filter(product=product, user=current_user)  
            existing_variation_list=[]
            id = []

            for item in cart_item:                
                existing_variation = item.variations.all()           
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            

            if product_variation in existing_variation_list:
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()               

            else:         
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation)>0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()            
                # cart_item.quantity += 1
        
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
            if len(product_variation)>0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()         
            print(cart_item.product)

        return redirect('cart')
   

    # #when user is not authenticated
    else:
        print("notauth")
        product_variation = []
        if request.method == 'POST':
            print('plus chech chec')

            # color = request.POST['color__radio']
            # size = request.POST['size']
            for item in request.POST:
                key = item
                value = request.POST[key]        
                print(key)
                print(value)

                try:  
                    
                    variation = Variation.objects.get(product=product, variation_value=value, variation_category=key)
                    print(variation) 
                    product_variation.append(variation)
                except:
                    pass                       
        
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request)) #get the cart using cart_id in the session

        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            

        cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:          
            cart_item = CartItem.objects.filter(product=product, cart=cart)  
            existing_variation_list=[]
            id = []

            for item in cart_item:
                # print('ji')
                existing_variation = item.variations.all()           
                existing_variation_list.append(list(existing_variation))
                id.append(item.id)
            print(existing_variation_list)
            print(product_variation)
            # product_variation.reverse()
            # print(product_variation)

            if product_variation in existing_variation_list:
                # print("kikiki")
                index = existing_variation_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:         
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation)>0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
                # cart_item.quantity += 1
        
        else:
            cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation)>0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
            print(cart_item.product)

        return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
   
    product = get_object_or_404(Item, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    
    except:
        pass
    return redirect('cart')  

def remove_cart_item(request, product_id, cart_item_id):
    if request.user.is_authenticated:
        product = get_object_or_404(Item, id=product_id)
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Item, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total) / 100
        grand_total = total + tax

    except ObjectDoesNotExist:
       pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' :grand_total,
    }
    return render(request, 'cart/cart.html',context)

@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):    
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            print('valid')
            data = Address()
            data.user = request.user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data ['address_line_2']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.city = form.cleaned_data['city']
            data.pincode = form.cleaned_data['pincode']
            
            data.save()
            return redirect('checkout')
        else:
            print("nottt")
    try:
       
        tax = 0
        grand_total = 0
        print("hi")
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
            address = Address.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))                 
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2*total) / 100
        grand_total = total + tax
        
    except ObjectDoesNotExist:
        pass

    context = {
        'total' : total,
        'quantity' : quantity,
        'cart_items' : cart_items,
        'tax' : tax,
        'grand_total' :grand_total,
        'address' : address,
    }
    return render(request, 'cart/checkout.html',context)


