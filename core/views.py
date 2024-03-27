from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Product, ProductReview, Category, wishlist, ClientChat, Notification, Address
from .forms import ProductReviewForm, ClientChatForm, UpdateProfileForm
from django.db.models import Avg
from taggit.models import Tag
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.utils.text import slugify
from django.template.loader import render_to_string
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from userauths.forms import ContactForm
# Create your views here.



def index(request):
    products = Product.objects.filter(
        Q(category__in=[1, 3, 8, 5, 6, 4, 7]) &  # Filter by categories
        Q(product_status="published")  # Additional filters
    )
    automobiles = products.filter(category=1)[:5]
    real_estate = products.filter(category=3)[:3]
    rentage = products.filter(category=8)[:1]
    furnitures = products.filter(category=5)[:1]
    fittings = products.filter(category=6)[:1]
    constructions = products.filter(category=4)[:1]
    materials = products.filter(category=7)[:1]
    wishlist_entries = {}  # Dictionary to store wishlist entries for each product
    
    if request.user.is_authenticated:
        # If the user is authenticated, get wishlist entries for all products at once
        wishlist_products = wishlist.objects.filter(product__in=products, user=request.user)
        for entry in wishlist_products:
            wishlist_entries[entry.product_id] = True

    context = {
        "automobiles": automobiles,
        "real_estate": real_estate,
        "rentage": rentage,
        "furniture": furnitures,
        "fittings": fittings,
        "constructions": constructions,
        "materials": materials,
        "wishlist_entries": wishlist_entries,
    }
    return render(request, "core/index.html", context)



def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context = {
        "products": products,
        "tag": tag,


    }
    return render(request, "core/tag.html", context)


def automobile_view(request):
    return render(request, "core/automobile.html")

def automobile_detail_view(request,pid):
    product = Product.objects.get(pid=pid)
    wishlist_count = wishlist.objects.filter(product=product).count()
    item_views = request.session.get('item_views', {})
    wishlist_entry = None
    if request.user.is_authenticated:
        wishlist_entry = wishlist.objects.filter(product=product, user=request.user).exists()

    
    products = Product.objects.filter(category=product.category).exclude(pid=pid).order_by('?')[:5]
    p_image = product.p_images.all()
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    # Getting average reviews
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # product review form 
    review_form = ProductReviewForm()
    make_chat = True

    if request.user.is_authenticated:
        user_chat_count = ClientChat.objects.filter(user=request.user, product=product).count()
        if user_chat_count > 0:
            make_chat = False
    context = {
        "p": product,
        "make_chat": make_chat,
        "p_image": p_image,
        "products": products,
        "reviews": reviews,
        "review_form": review_form,
        "average_rating": average_rating,
        "wishlist_entry": wishlist_entry,
        'wishlist_count': wishlist_count,
    }
    return render(request, "core/product-single.html", context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status= "published", category=category)[:12]
    total_data = Product.objects.filter(product_status= "published", category=category).count()
    sort_by = request.GET.get('sort_by', 'default')


    if sort_by == 'oldest':
        products = products.order_by('date') 
    elif sort_by == 'newest':
        products = products.order_by('-date') 
    context = {
        "category": category,
        "products": products,
        "total_data":total_data,

    }
    return render(request, "core/category-product-list.html", context)

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories": categories
    }
    return render(request, 'core/category-list.html', context)

def add_to_wishlist(request):
    product_id = request.POST.get('id')
    product = Product.objects.get(id=product_id)
    context = {}

    wishlist_count = wishlist.objects.filter(product=product, user=request.user).count()
    if wishlist_count > 0:
        context = {
            "bool": True,
        }
    else:
        new_wishlist = wishlist.objects.create(
            product=product,
            user=request.user,
        )
        product.in_wishlist = True
        product.save()
    context = {
        "bool": True
    }
    return JsonResponse(context)

def delete_from_wishlist(request):
    if request.method == 'POST':
        product_id = request.POST.get('id')
        try:
            product = Product.objects.get(id=product_id)
            product.in_wishlist = False
            product.save()
            wishlist_item = wishlist.objects.get(product=product, user=request.user)
            wishlist_item.delete()
            
            context = {"success": True}
        except ObjectDoesNotExist:
            context = {"success": False, "error": "Product not found in wishlist."}
        return JsonResponse(context)
    else:
        context = {"success": False, "error": "Invalid request method."}
        return JsonResponse(context)

def view_wishlist(request):
    
    if request.user.is_authenticated:
        wishlist_items = wishlist.objects.filter(user=request.user)
    else:
        wishlist_items = None

    return render(request, 'core/wishlist.html', {'wishlist_items': wishlist_items})

def contact_view(request):
    return render(request, "core/contact.html")

def submit_contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True,})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})


def about_view(request):
    return render(request,"core/about.html")


def faq_view(request):
    return render(request, "core/faq.html")


def search_view(request): 
    query = request.GET.get('q')
    category_title = request.GET.get('category')
    category = Category.objects.get(title=category_title)
    if query:
        if category_title:
            items = Product.objects.filter(category__title=category_title, title__icontains=query)
        else:
            items = Product.objects.filter(title__icontains=query)
        request.session['search_query'] = query
        request.session['search_results'] = list(items.values_list('id', flat=True))
        return render(request, 'core/search.html', {'products': items, 'query': query, 'category': category})
    else:
        items = Product.objects.all()

    return render(request, 'core/search.html', {'products': items, "query": query, "category_title": category_title,"category":category })

#load more
def load_more(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset+limit]
    t = render_to_string('ajax/category-product-list.html',{'data': data})
    return JsonResponse({'data':t})


def submit_inquiry(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = ClientChatForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
           
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        return JsonResponse({'success': False, 'errors': 'Invalid request method'})
    

def account_settings(request):
    return render(request, 'user/account-settings.html')

def update_password(request):

    return render(request, 'user/login-and-security.html')

def change_password(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return JsonResponse({'message': 'Password updated successfully', 'bool': True}, status=200)
        else:
            errors = form.errors
            return JsonResponse({'errors': errors, 'bool':False}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method', 'bool':False}, status=405)
    



def notifications(request):
    user = request.user
    notifications = user.notifications.all()
    return render(request, 'user/notifications.html', {'notifications': notifications})


def mark_as_read(request, notification_id):
    notification = get_object_or_404(Notification, pk=notification_id)
    if notification.recipient == request.user:
        notification.mark_as_read()
    return redirect('core:notifications')

def account_info(request):
    return render(request, 'user/account-info.html')


def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            response_data = {
                'success': True,
                'full_name': user.full_name,
                'phone_number': user.phone_number
            }
            return JsonResponse(response_data)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

def chat_page(request):
    chats = ClientChat.objects.filter(user=request.user)
    context = {
        'chats': chats
    }
    return render(request, 'user/chat-page.html', context)


def terms(request):
    return render(request, "core/terms.html")


def privacy(request):
    return render(request, "core/privacy.html")