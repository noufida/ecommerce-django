# from unicodedata import category
# from django.http import JsonResponse
from ast import Sub
from django.shortcuts import get_object_or_404, render, redirect
from cart.views import _cart_id
from cart.models import CartItem
from .models import Item,Section, Wish
from categories.models import Category,SubCategory
from django.http import HttpResponse
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request): 
    product = Item.objects.all().order_by('-id')[0:8]
    carousal = SubCategory.objects.all()
    section = Section.objects.all().order_by('-id')[0:3]
    women = SubCategory.objects.filter(gender__startswith = 'W')
    men = SubCategory.objects.filter(gender__startswith = 'M')    
    category = Category.objects.all()
    context = {
        'product' : product,
        'carousal' : carousal,
        'section' : section,
        'women' : women,
        'men' : men,   
        'category' : category,
    }   
    return render(request, 'item/index.html',context)

def shop(request,slug=None,sub_slug=None):
    categories = None
    categories = None
    subcategories = None
    products = None
    women = SubCategory.objects.filter(gender__startswith = 'W')
    men = SubCategory.objects.filter(gender__startswith = 'M')
    
    
    if slug != None:
        categories = get_object_or_404(Category,slug = slug)
        products = Item.objects.filter(category = categories)
        paginator = Paginator(products, 6   )
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        if request.method == 'POST':
            sort = request.POST['sort']
            if sort == 'inc':
                products = Item.objects.filter(category = categories).order_by('price')
                paginator = Paginator(products, 6)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)

            else:
                products = Item.objects.filter(category = categories).order_by('-price')
                paginator = Paginator(products, 6)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)


        if sub_slug != None:
            subcategories = get_object_or_404(SubCategory,slug = sub_slug)    
            products = Item.objects.filter(subcategory = subcategories)
            paginator = Paginator(products, 6)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)          
            if request.method == 'POST':
                sort = request.POST['sort']
                if sort == 'inc':
                    products = Item.objects.filter(subcategory = subcategories).order_by('price')
                    paginator = Paginator(products, 6)
                    page = request.GET.get('page')
                    paged_products = paginator.get_page(page)

                else:
                    products = Item.objects.filter(subcategory = subcategories).order_by('-price')
                    paginator = Paginator(products, 6)
                    page = request.GET.get('page')
                    paged_products = paginator.get_page(page)

    else:
        products = Item.objects.all().order_by('-id')
        paginator = Paginator(products, 9)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        if request.method == 'POST':
            sort = request.POST['sort']
            if sort == 'inc':
                products = Item.objects.all().order_by('price')
                paginator = Paginator(products, 9)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)

            else:
                products = Item.objects.all().order_by('-price')
                paginator = Paginator(products, 9)
                page = request.GET.get('page')
                paged_products = paginator.get_page(page)
        # product_count = products.count()
    context = {
        'products' : paged_products,
        'women' : women,
        'men' : men,
        'categories' : categories,
        # 'inc_price' : inc_price,
        
        # 'product_count' : product_count,
    }  
    
    return render(request,'item/shop.html',context)

def product_detail(request,slug,sub_slug,pro_slug):
    try:
        single_product = Item.objects.get(category__slug=slug,subcategory__slug=sub_slug, slug=pro_slug)
        in_cart = CartItem.objects.filter(cart__cart_id = _cart_id(request), product=single_product).exists()
        related_product = Item.objects.all().filter(subcategory__slug=sub_slug)[0:4]
    except Exception as e:
        raise e

    context = {
        'single_product' : single_product,
        'related_product' : related_product,
        'in_cart' : in_cart
    }
    return render(request,'item/product_detail.html',context)

def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        if q:
            products = Item.objects.order_by('-id').filter(Q(description__icontains=q) | Q(name__icontains=q) |  Q(brand__brand_name__icontains=q) |  Q(category__title__icontains=q) | Q(subcategory__name__icontains=q)   )   
            products_count = products.count()

        else:
            return redirect('shop')
    context = { 
        'products' : products,
        'products_count' : products_count,
    }
    return render(request, 'item/shop.html',context)

@ login_required(login_url='login')
def wish(request, id):
    
    product = Item.objects.get(id=id)
    check = Wish.objects.filter(product=product).exists()
    
    if not check:
        wishlist = Wish()
        wishlist.user = request.user
        wishlist.product = product
        wishlist.save()
   
    return redirect('index')
    
@ login_required(login_url='login')
def wish_render(request):
    product = Wish.objects.filter(user=request.user)
    context = {      
      'wishproduct': product,
    }

    return render(request, 'item/wish.html',context)

def remove_wish(request, id):
    product = Wish.objects.get(id=id)
    product.delete()
    return redirect('wish_render')
