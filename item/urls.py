from django.urls import path
from . import views


urlpatterns = [
   
    path('',views.index,name='index'),
    path('shop/',views.shop,name='shop'),
    path('shop/<slug:slug>/',views.shop,name='shop_by_category'),
    path('shop/<slug:slug>/<slug:sub_slug>/',views.shop,name='shop_by_subcategory'),
    path('shop/<slug:slug>/<slug:sub_slug>/<slug:pro_slug>',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),    
    path('wish/', views.wish_render, name='wish_render'),
    path('wish/<int:id>', views.wish, name='wish'),
    path('remove_wish/<int:id>', views.remove_wish, name='remove_wish'),
]


