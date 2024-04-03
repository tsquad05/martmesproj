from django.urls import path
from .views import (index, tag_list, contact_view, about_view, faq_view, search_view,
                    automobile_view, automobile_detail_view, chat_page, terms,
                    category_product_list_view, notifications, mark_as_read, privacy,
                    category_list_view, add_to_wishlist, view_wishlist, delete_from_wishlist, load_more, submit_inquiry,
                    account_settings, update_password, change_password, account_info, update_profile, submit_contact_view)

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
    path('listings/listing/<pid>', automobile_detail_view, name="listing-detail" ),
    path('add-to-wishlist/', add_to_wishlist, name='add_to_wishlist'),
    path('delete-from-wishlist/', delete_from_wishlist, name='delete_from_wishlist'),
    path('wishlist/', view_wishlist, name='view_wishlist'),
    path('load-more-data/', load_more, name='load-more-data'),
    path('submit_inquiry/', submit_inquiry, name='submit_inquiry'),
    path('user/account-settings/', account_settings, name='account_settings'),
    path('user/account-settings/update-password/', update_password, name='update-password'),
    path('user/account-settings/change-user-password/', change_password, name='change-password'),
    path('user/account-settings/notifications/', notifications, name='notifications'),
    path('user/account-settings/notifications/<int:notification_id>/mark_as_read/', mark_as_read, name='mark_as_read'),
    path('user/account-settings/account-information/', account_info, name='account_info'),
    path('user/update-profile/', update_profile, name='update_profile'),
    path('submit-contact/', submit_contact_view, name='submit_contact'),
    path('user/account-settings/chats/', chat_page, name="chat_page" ),
    path('terms-of-use/', terms, name="terms" ),
    path('privacy-policy/', privacy, name="privacy" )
]
