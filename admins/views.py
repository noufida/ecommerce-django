from django.shortcuts import render,redirect
from user.models import Account
from order.models import OrderProduct,Payment
from item.models import Item,Variation,Section,Brand,Review
from categories.models import Category,SubCategory
from .forms import CategoryEditForm, SubCategoryEditForm, ItemCreateForm, SectionForm, DiscountCouponForm,BrandForm, OrderForm,VariationForm
from django.contrib import messages,auth
from cart.models import  DiscountCoupon
from order.models import Order,OrderProduct
from django.db.models import Q


from django.db.models import Sum
from django.http import JsonResponse
# Create your views here.

from django.contrib.auth.decorators import user_passes_test

a=Account.objects.filter(is_superadmin=True)
 
@user_passes_test(lambda u: u in a, login_url='admin_login')
def admin_tab(request):
  
    total_amount=0
    customer_count = Account.objects.filter(is_superadmin=False).count()
    order_count = OrderProduct.objects.filter(ordered=True).count()
    ordered_pro = OrderProduct.objects.filter(ordered=True)
    amounts = Payment.objects.all()
    for x in ordered_pro:
       total_amount += x.product_price 

    item_count = Item.objects.all().count()

    context = {
        'customer_count':customer_count,
        'order_count' : order_count,
        'total_amount' : total_amount,
        'item_count' : item_count,
        'amounts' : amounts,
     
    }
    return render(request, 'admins/tables.html',context)


def product_chart(request):
    labels = []
    data = []

    queryset = OrderProduct.objects.values('product__name').annotate(count=Sum('quantity')).order_by('-id')[:7]
    for entry in queryset:
        labels.append(entry['product__name'])
        data.append(entry['count'])

    return JsonResponse (data= {
        
        'labels': labels,
        'data': data,
    })
    
def brand_chart(request):
    labels = []
    data = []

    queryset = OrderProduct.objects.values('product__subcategory__name').annotate(count=Sum('quantity')).order_by('-id')[:7]
    for entry in queryset:
        labels.append(entry['product__subcategory__name'])
        data.append(entry['count'])

    return JsonResponse (data= {
        
        'labels': labels,
        'data': data,
    })

# def brand_chart(request):
#     labels = []
#     data = []

#     queryset = OrderProduct.objects.values('subcategory__name').annotate(count=Sum('quantity')).order_by('-id')[:7]
#     for entry in queryset:
#         labels.append(entry['subcategory'])
#         data.append(entry['quantity'])

#     return JsonResponse (data= {
        
#         'labels': labels,
#         'data': data,
#     })




@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_user(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            users = Account.objects.order_by('-id').filter(Q(first_name__icontains=q) | Q(last_name__icontains=q) |  Q(email__icontains=q) )   
            # users_count = users.count()
            if not users.exists():
                messages.error(request, 'No Matching Datas')
                return render(request,'admins/manage_user.html')
        else:           
            return redirect('manage_user')
    else:
        users = Account.objects.filter(is_superadmin=False).order_by('-id')
    context = {
        'users' : users,
    }
    return render(request, 'admins/manage_user.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def block_user(request,id):
    account = Account.objects.get(id=id)

    if account.is_active:
        account.is_active = False
        account.save()
    else:
        account.is_active = True
        account.save()
    return redirect('manage_user')


@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_category(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            category = Category.objects.order_by('-id').filter(Q(title__icontains=q) )   
            # users_count = users.count()
            if not category.exists():
                messages.error(request, 'No Matching Datas Found')
                return render(request,'admins/categories.html')
        else:           
            return redirect('manage_category')
    else:
        category = Category.objects.all()
   
    context = {
        'category' : category,
    }
    return render(request, 'admins/categories.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def delete_category(request,id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('manage_category')

@user_passes_test(lambda u: u in a, login_url='admin_login')
def edit_category(request,id):
    category = Category.objects.get(id=id)
    form = CategoryEditForm(instance=category)
    try:
        if request.method == 'POST':
            form=CategoryEditForm(request.POST,instance=category)
            if form.is_valid():
                form.save()           
                return redirect('manage_category')
    except:
        messages.error(request, "Slug already exists.")
        print("slug exists")
        return redirect('edit_category')

    context={
        'form':form
        }    
    return render (request,'admins/edit_category.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def add_category(request):
    try:
        if request.method == 'POST':
            title = request.POST['title']
            slug = request.POST['slug']
            category = Category.objects.create(title=title, slug=slug)
            category.save()
            return redirect('manage_category')
        return render(request, 'admins/add_category.html')
    except:
        messages.error(request, "Slug already exists.")
        return redirect('add_category')



@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_subcategory(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            subcategory = SubCategory.objects.order_by('name').filter(Q(category__title__icontains=q) | Q(name__icontains=q) | Q(gender__icontains=q) )   
            # users_count = users.count()
            if not subcategory.exists():
                messages.error(request, 'No Matching Datas Found')
                return render(request,'admins/subcategories.html')
        else:           
            return redirect('manage_subcategory')
    else:
        subcategory = SubCategory.objects.all().order_by('name')
   
    context = {
        'subcategory' : subcategory,
    }
    return render(request, 'admins/subcategories.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def delete_subcategory(request,id):
    subcategory = SubCategory.objects.get(id=id)
    subcategory.delete()
    return redirect('manage_subcategory')

@user_passes_test(lambda u: u in a, login_url='admin_login')
def edit_subcategory(request,id):
    subcategory = SubCategory.objects.get(id=id)
    form = SubCategoryEditForm(instance=subcategory)
    try:
        if request.method == 'POST':
            form=SubCategoryEditForm(request.POST,request.FILES, instance=subcategory)
            if form.is_valid():
                form.save()           
                return redirect('manage_subcategory')
    except:
        messages.error(request, "Slug already exists.")
        print("slug exists")
        return redirect('edit_subcategory')

    context={
        'form':form
        }    
    return render (request,'admins/edit_subcategory.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def add_subcategory(request):
    form = SubCategoryEditForm
    try:
        if request.method == 'POST':
            form = SubCategoryEditForm(request.POST, request.FILES)
            if form.is_valid():
                print("yes")
                form.save()
                return redirect('manage_subcategory')
            else:
                print("no")
        return render(request, 'admins/add_subcategory.html',{'form':form})
    except:
        messages.error(request, "Slug already exists.")
        return redirect('add_subcategory')



@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_product(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            product = Item.objects.order_by('-id').filter(Q(category__title__icontains=q) | Q(subcategory__name__icontains=q) |Q(gender__icontains=q) | Q(brand__brand_name__icontains=q) |  Q(name__icontains=q))   
            # users_count = users.count()
            if not product.exists():
                messages.error(request, 'No Matching Datas Found')
                return render(request,'admins/product.html')
        else:           
            return redirect('manage_product')
    else:
        product = Item.objects.all().order_by('-id')

    context = {
        'product' : product,
    }
    return render(request, 'admins/product.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def add_product(request):
    form = ItemCreateForm
    try:
        if request.method == 'POST':
            form = ItemCreateForm(request.POST, request.FILES)
            if form.is_valid():
                print("yes")
                form.save()
                return redirect('manage_product')
           
        return render(request, 'admins/add_product.html',{'form':form})
    except:
        messages.error(request, "Slug already exists.")
        return redirect('add_subcategory')

def load_subcategory(request):
    category_id = request.GET.get('category')
    subcategory = SubCategory.objects.filter(category_id=category_id).order_by('name')
    return render(request, 'admins/dropdown.html', {'subcategory': subcategory})

@user_passes_test(lambda u: u in a, login_url='admin_login')
def delete_product(request,id):
    item = Item.objects.get(id=id)
    item.delete()
    return redirect('manage_product')

@user_passes_test(lambda u: u in a, login_url='admin_login')
def edit_product(request,id):
    item = Item.objects.get(id=id)
    form = ItemCreateForm(instance=item)
    try:
        if request.method == 'POST':
            form=ItemCreateForm(request.POST,request.FILES, instance=item)
            if form.is_valid():
                form.save()           
                return redirect('manage_product')
    except:
        messages.error(request, "Slug already exists.")
        print("slug exists")
        return redirect('edit_product')

    context={
        'form':form
        }    
    return render (request,'admins/add_product.html',context)



@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_variation(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            variation = Variation.objects.order_by('-id').filter(Q(product__name__icontains=q) | Q(variation_category__icontains=q) |Q(variation_value__icontains=q) )   
            # users_count = users.count()
            if not variation.exists():
                messages.error(request, 'No Matching Datas Found')
                return render(request,'admins/variation.html')
        else:           
            return redirect('manage_variation')
    else:   
        variation = Variation.objects.all().order_by('-product')

    context = {

        'variation' : variation,
    }
    return render(request, 'admins/variation.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def add_variation(request):
    form = VariationForm

    if request.method == 'POST':
        form = VariationForm(request.POST, request.FILES)
        if form.is_valid():            
            form.save()
            return redirect('manage_variation')
        
    return render(request, 'admins/add_variation.html',{'form':form})

@user_passes_test(lambda u: u in a, login_url='admin_login')
def edit_variation(request,id):
    variation = Variation.objects.get(id=id)
    form = VariationForm(instance=variation)
  
    if request.method == 'POST':
        form=VariationForm(request.POST,instance=variation)
        if form.is_valid():
            form.save()           
            return redirect('manage_variation')
   
    context={
        'form':form
        }    
    return render (request,'admins/add_variation.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def delete_variation(request,id):
    variation = Variation.objects.get(id=id)
    variation.delete()
    return redirect('manage_variation')



@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_section(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            section = Section.objects.order_by('-id').filter(Q(name__icontains=q)  )   
            # users_count = users.count()
            if not section.exists():
                messages.error(request, 'No Matching Datas Found')
                return render(request,'admins/section.html')
        else:           
            return redirect('manage_section')
    else:
        section = Section.objects.all().order_by('name')

    context = {
        'section' : section,
    }
    return render(request, 'admins/section.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def add_section(request):
    form = SectionForm
   
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('manage_section')
        
    return render(request, 'admins/add_section.html',{'form':form})

@user_passes_test(lambda u: u in a, login_url='admin_login') 
def delete_section(request,id):
    section = Section.objects.get(id=id)
    section.delete()
    return redirect('manage_section')

@user_passes_test(lambda u: u in a, login_url='admin_login')
def edit_section(request,id):
    section = Section.objects.get(id=id)
    form = SectionForm(instance=section)

    if request.method == 'POST':
        form=SectionForm(request.POST,instance=section)
        if form.is_valid():
            form.save()           
            return redirect('manage_section')


    context={
        'form':form
        }    
    return render (request,'admins/add_section.html',context)



@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_discount(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            coupon = DiscountCoupon.objects.order_by('-id').filter(Q(coupon_code__icontains=q)  )   
            # users_count = users.count()
            if not coupon.exists():
                messages.error(request, 'No Matching Datas Found')
                return render(request,'admins/coupon.html')
        else:           
            return redirect('manage_discount')
    else:
        coupon = DiscountCoupon.objects.all().order_by('-id')

    context = {
        'coupon' : coupon,
    }
    return render(request, 'admins/coupon.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def add_discount(request):
    form = DiscountCouponForm
   
    if request.method == 'POST':
        form = DiscountCouponForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('manage_discount')
        
    return render(request, 'admins/add_discount.html',{'form':form})

@user_passes_test(lambda u: u in a, login_url='admin_login')
def delete_discount(request,id):
    discount = DiscountCoupon.objects.get(id=id)
    discount.delete()
    return redirect('manage_discount')

@user_passes_test(lambda u: u in a, login_url='admin_login')
def edit_discount(request,id):
    discount = DiscountCoupon.objects.get(id=id)
    form = DiscountCouponForm(instance=discount)

    if request.method == 'POST':
        form=DiscountCouponForm(request.POST,instance=discount)
        if form.is_valid():
            form.save()           
            return redirect('manage_discount')


    context={
        'form':form
        }    
    return render (request,'admins/add_discount.html',context)



@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_order(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            order = Order.objects.order_by('-id').filter(Q(user__first_name__icontains=q) | Q(order_number__icontains=q))  
            order_product = OrderProduct.objects.all()
            # users_count = users.count()
            if not order.exists():
             
                return render(request,'admins/order.html')
        else:           
            return redirect('manage_order')
    else:
        order = Order.objects.all().order_by('-id')
        order_product = OrderProduct.objects.all()
    context = {
        'order' : order,
        'order_product' :  order_product,
    }
    return render(request, 'admins/order.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def edit_order(request,id):
    order = Order.objects.get(id=id)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form=OrderForm(request.POST,instance=order)
        
        if form.is_valid():
            form.save()                  
            return redirect('manage_order')

    context={
        'form':form,       
        }    
    return render (request,'admins/edit_order.html',context)



@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_brand(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            brand = Brand.objects.order_by('-id').filter(Q(brand_name__icontains=q)  )   
            # users_count = users.count()
            if not brand.exists():
                messages.error(request, 'No Matching Datas Found')
                return render(request,'admins/brand.html')
        else:           
            return redirect('manage_brand')
    else:
        brand = Brand.objects.all().order_by('-id')

    context = {
        'brand' : brand,
    }
    return render(request, 'admins/brand.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def edit_brand(request,id):
    brand = Brand.objects.get(id=id)
    form = BrandForm(instance=brand)

    if request.method == 'POST':
        form=BrandForm(request.POST,instance=brand)
        if form.is_valid():
            form.save()           
            return redirect('manage_brand')


    context={
        'form':form
        }    
    return render (request,'admins/add_brand.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def delete_brand(request,id):
    brand = Brand.objects.get(id=id)
    brand.delete()
    return redirect('manage_brand')

@user_passes_test(lambda u: u in a, login_url='admin_login')
def add_brand(request):
    form = BrandForm
   
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            
            form.save()
            return redirect('manage_brand')
        
    return render(request, 'admins/add_brand.html',{'form':form})

@user_passes_test(lambda u: u in a, login_url='admin_login')
def manage_review(request):
    
    review = Review.objects.all().order_by('-id')

    context = {
        'review' : review,
    }
    return render(request, 'admins/review.html',context)

@user_passes_test(lambda u: u in a, login_url='admin_login')
def delete_review(request,id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('manage_review')


def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
     
        user = auth.authenticate(email=email, password=password)
        
        if user is not None:
         
            if user.is_superadmin:
                auth.login(request,user)
                return redirect('admin_tab')          
         
            auth.login(request, user)       


        else:
            messages.error(request,'Invalid login Credentials!!')
            return redirect('admin_login')
   
    return render (request, 'admins/admin_login.html')


@user_passes_test(lambda u: u in a, login_url='admin_login')
def admin_logout(request):
    auth.logout(request)
    messages.success(request,'You were logged out')
    return redirect('admin_login')