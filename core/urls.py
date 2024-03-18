from django.urls import path
from .views import (index, tag_list, contact_view, about_view, faq_view, search_view,
                    automobile_view, automobile_detail_view,
                    category_product_list_view,
                    category_list_view, add_to_wishlist, view_wishlist, delete_from_wishlist)

app_name = "core"

urlpatterns = [
    path('', index, name="index" ),
    path('contact/', contact_view, name="contact" ),
    path('about/', about_view, name="about" ),
    path('FAQs/', faq_view, name="faq" ),
    path('search/', search_view, name='search'),
    path('categories/', category_list_view, name="categories" ),
    path('categories/<cid>', category_product_list_view, name="category-product-list" ),
    path("listings/tag/<slug:tag_slug>/", tag_list, name='tags'),
    path('automobiles/', automobile_view, name="automobile" ),
    path('listing/<pid>', automobile_detail_view, name="listing-detail" ),
    path('add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('delete-from-wishlist/', delete_from_wishlist, name='delete_from_wishlist'),
    path('wishlist/', view_wishlist, name='view_wishlist'),
]
