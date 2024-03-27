import random
import string
import cloudinary
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.utils.dateformat import format
          
cloudinary.config( 
  cloud_name = getattr(settings, 'CLOUD_NAME', None), 
  api_key = getattr(settings, 'API_KEY', None), 
  api_secret = getattr(settings, 'API_SECRET', None)
)




def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)




STATUS_CHOICE = (
    ("process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)



STATUS = (
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected", "Rejected"),
    ("in_review", "In Review"),
    ("published", "Published"),
)



RATING = (
    (1, "⭐✩✩✩✩"),
    (2, "⭐⭐✩✩✩"),
    (3, "⭐⭐⭐✩✩"),
    (4, "⭐⭐⭐⭐✩"),
    (5, "⭐⭐⭐⭐⭐"),
)




class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=45, prefix="", alphabet="abcdefgh12345") #custom uuid field
    title = models.CharField(max_length=100)
    image = CloudinaryField()
    requires_payment = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def save(self, *args, **kwargs):
        # Generate a shorter version of the blog title
        shortened_title = self.title[:40]  # You can adjust the length as needed
        # Convert the shortened title to a slug
        slug = slugify(shortened_title)
        # Set the bid to the slug
        self.cid = f"{slug}"
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title




    
class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=45, prefix="", alphabet="abcdefgh12345") #product uuid field
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    title = models.CharField(max_length=100, default="Fresh Pear")
    image = CloudinaryField()
    image2 = CloudinaryField()

    # description = models.TextField(null=True, blank=True, default="This is the product")
    description = RichTextUploadingField(null=True, blank=True, default="This is the product")
    
    price = models.DecimalField(max_digits=100, decimal_places=2, default="0.99")
    consultant_price = models.DecimalField(max_digits=100, decimal_places=2, default="1.99")
    specifications = models.TextField(null=True, blank=True)
    # specifications = RichTextUploadingField(null=True, blank=True)
    
    tags = TaggableManager(blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)

    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    

    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    sku = ShortUUIDField(unique=True, length=10, max_length=20, prefix="sku", alphabet="1234567890") 
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)
    first_save = models.BooleanField(default=False)
    in_wishlist = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if not self.first_save:
           
            shortened_title = self.title[:40]  # You can adjust the length as needed
            # Convert the shortened title to a slug
            slug = slugify(shortened_title)
            # Set the pid to the slug
            random_int = ''.join(random.choices(string.digits, k=7))
            # Concatenate the slug and random integer to create pid
            self.pid = f"{slug}-{random_int}"
            self.first_save = True
        super().save(*args, **kwargs)
    



class ProductImages(models.Model):
    images = CloudinaryField()
    product = models.ForeignKey(Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product images"





###################################################### Cart, Order, OrderItems and Address ####################################################
###################################################### Cart, Order, OrderItems and Address ####################################################
###################################################### Cart, Order, OrderItems and Address ####################################################
###################################################### Cart, Order, OrderItems and Address ####################################################




class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=100, decimal_places=2, default="0.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")

    class Meta:
        verbose_name_plural = "Cart Order"

class CartOrderItems(models.Model):
    order = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200 )
    product_status = models.CharField(max_length=200 )
    item = models.CharField(max_length=200 )
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=100, decimal_places=2, default="0.99")
    total = models.DecimalField(max_digits=100, decimal_places=2, default="0.99")
    class Meta:
        verbose_name_plural = "Cart Order Items"
    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))


###################################################### Product, Review, Wishlist, Address ####################################################
###################################################### Product, Review, Wishlist, Address ####################################################
###################################################### Product, Review, Wishlist, Address ####################################################
###################################################### Product, Review, Wishlist, Address ####################################################





class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='reviews')
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Products Reviews"

    def __str__(self):
        return self.product.title
    def get_rating(self):
        return self.rating
    





class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "wishlists"

    def __str__(self):
        return self.product.title
    @classmethod
    def clear_wishlist(cls, user):
        """Clears all wishlist items for the specified user."""
        cls.objects.filter(user=user).delete()




class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name_plural = "Address"




class House(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    num_bedrooms = models.PositiveIntegerField(default=0)
    num_parking_spaces = models.PositiveIntegerField(default=0)
    num_bathrooms = models.PositiveIntegerField(default=0)
    num_toilets = models.PositiveIntegerField(default=0)

def ordinal(day):
    if 10 <= day % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return str(day) + suffix

def custom_strftime(t):
    return "{}, {} {} {}, at {}:{} {}".format(
        ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][t.weekday()],
        ordinal(t.day),
        ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][t.month-1],
        t.year,
        t.strftime('%I'),
        t.strftime('%M'),
        t.strftime('%p').lower()
    )

class ClientChat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    date_sent = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"Inquiry from {self.user.full_name} on {custom_strftime(self.date_sent)}"
    class Meta:
        verbose_name_plural = "Inquiries from client"


class Notification(models.Model):
    message = models.TextField()
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return self.message
