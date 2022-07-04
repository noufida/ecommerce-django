from django import forms
from categories.models import Category,SubCategory
from item.models import Item,Section,Variation,Brand
from cart.models import DiscountCoupon
from order.models import Order
from django.utils.text import slugify

class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title','slug',]
    def __init__(self, *args, **kwargs):
        super(CategoryEditForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})
   

class SubCategoryEditForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name','slug','gender', 'image',]

    def __init__(self, *args, **kwargs):
        
        super(SubCategoryEditForm, self).__init__(*args, **kwargs)        
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})


class ItemCreateForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['category', 'subcategory', 'gender', 'name', 'slug', 'brand', 'description', 'price', 
        'discount', 'stock', 'availability', 'section', 'image', 'image2', 'image3', 'image4' ]

    def __init__(self, *args, **kwargs):
        super(ItemCreateForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['subcategory'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['slug'].widget.attrs.update({'class': 'form-control'})
        self.fields['brand'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['discount'].widget.attrs.update({'class': 'form-control'})
        self.fields['stock'].widget.attrs.update({'class': 'form-control'})       
        self.fields['section'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['image2'].widget.attrs.update({'class': 'form-control'})
        self.fields['image3'].widget.attrs.update({'class': 'form-control'})
        self.fields['image4'].widget.attrs.update({'class': 'form-control'})



        self.fields['subcategory'].queryset = SubCategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = SubCategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(SectionForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(BrandForm, self).__init__(*args, **kwargs)
        self.fields['brand_name'].widget.attrs.update({'class': 'form-control'})
   
    


class DiscountCouponForm(forms.ModelForm):
    class Meta:
        model = DiscountCoupon
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(DiscountCouponForm, self).__init__(*args, **kwargs)
        self.fields['coupon_code'].widget.attrs.update({'class': 'form-control'})
        self.fields['discount'].widget.attrs.update({'class': 'form-control'})
        self.fields['active_from'].widget.attrs.update({'class': 'form-control'})
        



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status',]

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'form-control'})


class VariationForm(forms.ModelForm):
    class Meta:
        model = Variation
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VariationForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs.update({'class': 'form-control'})
        self.fields['variation_category'].widget.attrs.update({'class': 'form-control'})
        self.fields['variation_value'].widget.attrs.update({'class': 'form-control'})
       
      