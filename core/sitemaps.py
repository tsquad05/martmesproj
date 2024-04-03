from django.contrib.sitemaps import Sitemap
from django.db.models.base import Model
from django.urls import reverse
from .models import Category, Product

class StaticSitemap(Sitemap):
    def items(self):
        return ['core:index','core:about','core:contact','core:faq','core:categories','core:terms','core:privacy', 'userauths:login']
    def location(self, item):
        return reverse(item)
    
class CategorySitemap(Sitemap):
    def items(self):
        return Category.objects.all().order_by('-date')  
    
class ProductSitemap(Sitemap):
    def items(self):
        return Product.objects.all().order_by('-date')  