from pipes import Template
from django.db import models
from user.models import Account
from item.models import Item, Variation


# Create your models here.
class DiscountCoupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    discount = models.DecimalField(max_digits=6,decimal_places=2)
    active_from = models.DecimalField(max_digits=6,decimal_places=2)
    created_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.coupon_code

class Discount(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    discount_appleid = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return self.user.email

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank = True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    discount = models.ForeignKey(DiscountCoupon, on_delete=models.CASCADE,null=True,blank=True)

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product

