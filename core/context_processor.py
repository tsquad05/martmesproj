from core.models import Category, Product

def default(request):
    categories = Category.objects.all()
    user = request.user

    return {
        "categories": categories,
        "user": user,
    }

def recommended_products(request):
    recommended_products = None

    if 'search_query' in request.session:
        query = request.session['search_query']
        search_results_ids = request.session.get('search_results', [])
        
        if search_results_ids:
            try:
                category = Product.objects.get(id=search_results_ids[0]).category
                recommended_products = Product.objects.filter(category=category).exclude(id__in=search_results_ids)[:6]
            except Product.DoesNotExist:
                recommended_products = None

    return {'recommended_products': recommended_products}