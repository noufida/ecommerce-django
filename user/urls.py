from django.urls import path
from . import views

urlpatterns = [   
    path('register/',views.user_register,name='register'),
    path('login/',views.user_login,name='login'),
    path('',views.home,name='home'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.profile,name='profile'),
    path('order_history/',views.order_history,name='order_history'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('forgotpassword/',views.forgot_password,name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>',views.resetpassword_validate,name='resetpassword_validate'),
    path('resetpassword/',views.reset_password,name='resetpassword'), 
    path('verify/', views.verify_code,name="verify"),
    path('delete_address/<int:id>/', views.delete_address,name="delete_address"),
    path('edit_profile/<int:id>/', views.edit_profile,name="edit_profile"),
    path('review/<int:id>/',views.review,name='review'),
    path('change_password',views.change_password,name='change_password'),
    path('pdf/<int:id>/',views.ResultList,name='pdf'),
]

