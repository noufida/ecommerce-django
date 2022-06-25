
from django.db import models
from user.models import Account,Address
from item.models import Item,Variation
from cart.models import DiscountCoupon
# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100) 
    order_id = models.CharField(max_length=100, blank=True)  
    amount_paid = models.CharField(max_length=100)    
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id

class Order(models.Model):
    STATUS = (
        ('New' ,'New' ),
        ('Accepted', 'Accepted'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Failed', 'Failed'),
        ('Delivered', 'Delivered'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payement = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL,null=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    discount = models.ForeignKey(DiscountCoupon, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_number

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payement = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation,blank=True) 
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name

