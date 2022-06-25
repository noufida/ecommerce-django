from django.urls import path
from . import views

urlpatterns = [ 
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_logout/',views.admin_logout,name='admin_logout'),
    path('tables/',views.admin_tab,name='admin_tab'),
    path('product_chart/', views.product_chart, name='product_chart'),
    path('brand_chart/', views.brand_chart, name='brand_chart'),

    path('manage_user/',views.manage_user,name='manage_user'),
    path('block_user/<int:id>/',views.block_user,name='block_user'),

    path('manage_category/',views.manage_category,name='manage_category'),
    path('delete_category/<int:id>/',views.delete_category,name='delete_category'),
    path('edit_category/<int:id>/',views.edit_category,name='edit_category'),
    path('add_category/',views.add_category,name='add_category'),

    path('manage_subcategory/',views.manage_subcategory,name='manage_subcategory'),
    path('delete_subcategory/<int:id>/',views.delete_subcategory,name='delete_subcategory'),
    path('edit_subcategory/<int:id>/',views.edit_subcategory,name='edit_subcategory'),
    path('add_subcategory/',views.add_subcategory,name='add_subcategory'),

    path('manage_product/',views.manage_product,name='manage_product'),
    path('add_product/',views.add_product,name='add_product'),
    path('ajax/load-subcategory/', views.load_subcategory, name='ajax_load_subcategory'),
    path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
    path('edit_product/<int:id>/',views.edit_product,name='edit_product'),

    path('manage_brand/',views.manage_brand,name='manage_brand'),
    path('add_brand/',views.add_brand,name='add_brand'),
    path('edit_brand/<int:id>/',views.edit_brand,name='edit_brand'),
    path('delete_brand/<int:id>/',views.delete_brand,name='delete_brand'),

    path('manage_variation/',views.manage_variation,name='manage_variation'),
    path('add_variation/',views.add_variation,name='add_variation'),
    path('edit_variation/<int:id>/',views.edit_variation,name='edit_variation'),
    path('delete_variation/<int:id>/',views.delete_variation,name='delete_variation'),

    path('manage_section/',views.manage_section,name='manage_section'),
    path('add_section/',views.add_section,name='add_section'),
    path('delete_section/<int:id>/',views.delete_section,name='delete_section'),
    path('edit_section/<int:id>/',views.edit_section,name='edit_section'),

    path('manage_discount/',views.manage_discount,name='manage_discount'),
    path('add_discount/',views.add_discount,name='add_discount'),
    path('edit_discount/<int:id>/',views.edit_discount,name='edit_discount'),
    path('delete_discount/<int:id>/',views.delete_discount,name='delete_discount'),

    path('manage_order/',views.manage_order,name='manage_order'),
    path('edit_order/<int:id>/',views.edit_order,name='edit_order'),

    path('manage_review/',views.manage_review,name='manage_review'),
    path('delete_review/<int:id>/',views.delete_review,name='delete_review'),
]

