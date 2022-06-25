from django.contrib import admin
from .models import Item, Section, Brand, Variation, Wish, Review

# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','price','stock','subcategory','availability')
    prepopulated_fields = {'slug':('name',)}

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value','is_active')

admin.site.register(Section)
admin.site.register(Item, ItemAdmin)
admin.site.register(Brand)
admin.site.register(Variation,VariationAdmin)
admin.site.register(Wish)
admin.site.register(Review)