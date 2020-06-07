from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from cart.forms import CartAddProductForm


# Create your views here.

def product_list(request, category_slug=None):
    # Get list of products, filter by category_slug.
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        # Filter products by category.
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                  'categories': categories,
                  'products': products})

def product_detail(request, id, slug):
    # Get single product using id.
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)

    cart_product_form = CartAddProductForm()

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form})


