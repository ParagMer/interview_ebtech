from django.urls import path
from .views import product_api, productListing

urlpatterns = [
    path('products/', product_api, name='product-api'),
    path('productListing/', productListing, name='product-list'),
]