from django.contrib import admin
from django.forms import inlineformset_factory
from django import forms

from .models import Category, Product, ProductImages, ProductReview, wishlist, Address, CartOrderItems, CartOrder, House, ClientChat, Notification
# Register your models here.

HouseInlineFormSet = inlineformset_factory(Product, House, fields=('num_bedrooms', 'num_parking_spaces', 'num_bathrooms','num_toilets'), extra=1)

class HouseInline(admin.StackedInline):
    model = House
    fields = ('num_bedrooms', 'num_parking_spaces', 'num_bathrooms','num_toilets')


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class CategoryAdmin(admin.ModelAdmin):
    list_display = [ 'category_image','title',  'cid']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['product','user','date']
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin, HouseInline]
    list_display = ['product_image','title', 'consultant_price','price',"category"]
    exclude = ('first_save','updated','sku','pid','status','in_stock','in_wishlist')

    def get_inline_instances(self, request, obj=None):
        inlines = super().get_inline_instances(request, obj)
        if obj and obj.category.title == 'Real Estate':
            inlines = [inline for inline in inlines if not isinstance(inline, HouseInline)]
            inlines.append(HouseInline(self.model, self.admin_site))
        return inlines





class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date']


class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'review', 'rating', 'date']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(ClientChat)
admin.site.register(Notification)
