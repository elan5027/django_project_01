from django.urls import path

from . import views

urlpatterns = [
    path('', views.product_main, name='product_main'),
    path('product/', views.product_add, name='products_add'),
    path('inbound/', views.inbound_create, name='inbound_create'),
    path('outbound/', views.outbound_create, name='outbound_create'),
    path('category/', views.category_create, name='category_create'),
    path('detail/', views.detail_create, name='detail_create'),

    
]