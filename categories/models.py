from django.db import models
from django.urls import reverse

# Create your models here.
GENDER_CHOICES=[
    ('MEN','men'),
    ('WOMEN','women'),
]


class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,max_length=50)
   
    def get_url(self):
        return reverse('shop_by_category', args =[self.slug])

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES) 
    image = models.ImageField(upload_to = 'images', blank=True,null=True)

    def __str__(self):
        return self.category.title + ' | ' + self.name

    def get_url(self):
        return reverse('shop_by_subcategory', args =[self.category.slug, self.slug])

    def get_url_w(self):
        return reverse('shop_by_subcategory_women', args =[self.category.slug, self.slug])

    def get_url_m(self):
        return reverse('shop_by_subcategory_men', args =[self.category.slug, self.slug])