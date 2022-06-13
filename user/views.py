from cmath import log
from django.shortcuts import render,redirect
from .models import Account,Address
from .forms import RegistrationForm, VerifyForm, EditUserForm
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

#verification_email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

#twilio
from .verify import send,check

from cart.models import Cart,CartItem
from cart.views import _cart_id
from order.models import Payment
#dynamic url redirecting
# import   requests

# Create your views here.

def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            if Account.objects.filter(phone_number=phone_number).exists():
                messages.error(request,'Phone number already exists')
            # elif Account.objects.filter(phone_number=phone_number).exists():
            #     messages.error(request,'Phone number already exists')
            else:
                user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
                user.phone_number = phone_number
                user.save()
                request.session['phone_number']=phone_number
                send(form.cleaned_data.get('phone_number'))
                return redirect('verify')          
    else:       
        form = RegistrationForm()
    context = {
        'form' : form
    }
    return render(request, 'user/register.html',context)


def verify_code(request):
    if request.method == 'POST':
        
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_number= request.session['phone_number']
            if check(phone_number, code):
                user=Account.objects.get(phone_number=phone_number)
                user.is_active = True
                user.save()
                return redirect('login')
    else:
        form = VerifyForm()
    return render(request, 'user/verify.html', {'form': form})

# def user_register(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             phone_number = form.cleaned_data['phone_number']
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             username = email.split("@")[0]
#             user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
#             user.phone_number = phone_number
#             user.save()

#             current_site = get_current_site(request)
#             mail_subject = 'Please  activate your account'
#             message = render_to_string('user/account_verification_email.html',{
#                 'user' : user,
#                 'domain' : current_site,
#                 'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token' : default_token_generator.make_token(user),
#             })
#             to_email = email
#             send_email = EmailMessage(mail_subject, message, to=[to_email])
#             send_email.send()
#             # messages.success(request, 'Thankyou for registering with us. To complete the verification process, please check the email we have sent to you.')
#             return redirect('/user/login/?command=verification&email='+email)
#     else:       
#         form = RegistrationForm()
#     context = {
#         'form' : form
#     }
#     return render(request, 'user/register.html',context)

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    #getting product variation by cart id
                    product_variation = []
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    #get cart items from the user to access their product variations
                    cart_item = CartItem.objects.filter(user=user)  
                    existing_variation_list=[]
                    id = []

                    for item in cart_item: 
                        print("item present")               
                        existing_variation = item.variations.all()           
                        existing_variation_list.append(list(existing_variation))
                        id.append(item.id)
                        print(product_variation)
                        print(existing_variation_list)
                    for pr in product_variation:
                        if pr in existing_variation_list:
                            print("varn present")
                            index = existing_variation_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity +=1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            # "if 'ckeckout' in request.session :
            #     return redirect('checkout')
            # else:
            #     "
            # 
            return redirect('/')
            # url = request.META.get('HTTP_REFERER')
            # print(url)
            # try:
            #     print("hi")
            #     query = requests.util.urlparse(url).query
            #     print(query)
            #     print('--------')
            #     params = dict(x.split('=') for x in query.split('&'))
            #     print('param', params)
            #     if 'next' in params:
            #         nextPage = params['next']
            #         return redirect(nextPage)
               
            # except:
            #     return redirect('/')

            

        else:
            messages.error(request,'Invalid login Credentials!!')
            return redirect('login')
    return render(request, 'user/login.html')

def home(request):
    return render(request, 'user/home.html')

@login_required(login_url='login')
def user_logout(request):
    auth.logout(request)
    messages.success(request,'You were logged out')
    return redirect('index')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid Activation link')
        return redirect('register')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            #reset password email
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            message = render_to_string('user/reset_password_email.html',{
                'user' : user,
                'domain' : current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')

        else:
            messages.error(request,'Account Does not Exist.')
            return redirect('forgotpassword')

    return render(request, 'user/forgotpassword.html')

def resetpassword_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request,'This link has been expired')
        return redirect('login')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfull')
            return redirect('login')
        else:
            messages.error(request,'Passwords does not match!')
            return redirect('resetpassword')
    else:    
        return render(request, 'user/resetpassword.html')


@ login_required(login_url='login')
def profile(request):
    user = Account.objects.get(id=request.user.id)
    address = Address.objects.filter(user=user, )[0:1]
    # orders = Payment.objects.filter(user=request.user,paid=True)
    context = {
        'user' :user,
        'address' : address,
        # 'orders' : orders,
    }
    return render(request, 'user/profile.html',context)

def delete_address(request, id):
    user=request.user
    curr_address = Address.objects.get(user=user, id=id)
    curr_address.delete()   

    return redirect('checkout')

@login_required(login_url='login')
def edit_profile(request,id):
    try:
        account = Account.objects.get(id=id)
        print(account)
        form = EditUserForm(instance=account)
        if request.method ==  'POST':
            form = EditUserForm(request.POST, instance=account)
            if form.is_valid():
                form.save()
                return redirect('profile')
    except:
        return redirect('profile')

    context = {
        'form' : form,
    }
    return render(request,'user/edit_profile.html',context)