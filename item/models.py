
from django.db import models
from categories.models import *
from django.urls import reverse

from user.models import Account
# Create your models here.

GENDER_CHOICES=[
    ('MEN','men'),
    ('WOMEN','women'),
]

class Section(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Brand(models.Model):
    brand_name = models.CharField(max_length=50)
    def __str__(self):
        return self.brand_name 




class Item(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)   
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES) 
    name = models.CharField(max_length=50) 
    slug = models.SlugField(unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(max_length=200)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    discount = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
    stock = models.IntegerField()
    availability = models.BooleanField()
    section = models.ForeignKey(Section, on_delete=models.DO_NOTHING,blank=True,null=True)
    image = models.ImageField(upload_to='images',null=True,blank=True)
    image2 = models.ImageField(upload_to='images',null=True,blank=True)
    image3 = models.ImageField(upload_to='images',null=True,blank=True)
    image4 = models.ImageField(upload_to='images',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product_detail', args =[self.category.slug, self.subcategory.slug, self.slug])

class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color',is_active= True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size',is_active= True)

variation_category_choice = (
    ('color','color'),
    ('size','size'),
)

class Variation(models.Model):
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value

class Wish(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)


class Review(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Item, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='review',null=True,blank=True)
    review = models.TextField(max_length=300)
    rating = models.IntegerField(null=True,blank=True)
    created_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product.name

