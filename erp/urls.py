from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_main, name='product_main'),
    path('get_category/', views.get_category, name='get_category'),
    path('get_code/', views.get_code, name='get_code'),
    path('product/add/', views.product_add, name='products_add'),
    path('inbound/create/', views.inbound_create, name='inbound_create'),
    path('outbound/create/', views.outbound_create, name='outbound_create'),
    
]