from categories.models import Category,SubCategory

def menu_links(request):
    c_links = Category.objects.all()
    return dict(c_links= c_links)

def menu_links(request):
    s_links = SubCategory.objects.all()
    return dict(s_links= s_links)
    