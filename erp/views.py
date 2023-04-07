# tweet/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from .forms import ProductForm, InboundForm, OutboundForm, CategorySizeForm, CategoryForm
from .models import Product, Inbound, Outbound, CategorySize, Category
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse


def product_main(request):
    user = request.user.is_authenticated
    if user:
        products = Product.objects.all()
        return render(request, 'erp/home.html', {'products': products})
    else:
        return redirect('/user_login')


def category_create(request):
    if request.method == 'POST':
        print("TEST:")
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = {
            'category' : CategoryForm(),
        }
    return render(request, 'erp/category.html', {'form': form})

def detail_create(request):
    if request.method == 'POST':
        form = CategorySizeForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = {
            'size' : CategorySizeForm(),
        }
    return render(request, 'erp/codesize.html', {'form': form})


@login_required
@transaction.atomic
def product_add(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('/')
    else:
        form = ProductForm()
    return render(request, 'erp/product_add.html', {'form': form})


@login_required
def inbound_create(request):
    if request.method == 'POST':
        form = InboundForm(request.POST)
        try:
            with transaction.atomic():

                if form.is_valid():
                    inbound = form.save(commit=False)
                    inbound.save()

                    product = inbound.product
                    quantity = inbound.quantity
                    if quantity < 0:
                        raise Exception("음수값은 입력할수 없습니다.")
                    Product.objects.filter(name=product).update(stock_quantity=F('stock_quantity') + quantity)
                    return redirect('/')
        except Exception as e:
            form = InboundForm()
            context = {
                'form': form,
                'error': e,
            }
            return render(request, 'erp/inbound.html', context)
    else:
        form = InboundForm()

        context = {
            'form': form,
        }

    return render(request, 'erp/inbound.html', context)


@login_required
def outbound_create(request):
    if request.method == 'POST':
        form = OutboundForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid():
                    outbound = form.save(commit=False)
                    outbound.save()

                    product = outbound.product
                    quantity = outbound.quantity
                    quantity_check = Product.objects.filter(name=product).values('stock_quantity').first()
                    if (quantity_check['stock_quantity'] - quantity) < 0:
                        raise Exception("해당 물품의 갯수만큼의 상품이 없습니다.")
                    if quantity < 0:
                        raise Exception("음수값은 입력할수 없습니다.")
                    Product.objects.filter(name=product).update(stock_quantity=F('stock_quantity') - quantity)

                    return redirect('/')
        except Exception as e:
            form = OutboundForm()
            context = {
                'form': form,
                'error': e,
            }
            return render(request, 'erp/outbound.html', context)
    else:
        form = OutboundForm()

        context = {
            'form': form,
        }

    return render(request, 'erp/outbound.html', context)

