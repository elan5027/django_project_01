# tweet/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView
from .forms import ProductForm, InboundForm, OutboundForm
from .models import Product, Inbound, Outbound
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


def get_category(request):
    item = request.GET.get('item')
    # doc2 = [x[1] for x in Product.categorys ]
    # 나중에 수정 A,B,C size 수치도 딕셔너리로 받아오고 자동생성하게.
    doc = {
        'Hood': ('S', 'M', 'L', 'XL'),
        'Jean': 'FREE',
        'Socks': ('M', 'S', 'L', 'FREE'),
        'Hat': 'FREE',
    }
    return JsonResponse({"result": doc[item]})


def get_code(request):

    item = request.GET.get('item')
    doc = {
        'Hood': ('hood-001', 'hood-002', 'hood-003'),
        'Jean': 'jean-001',
        'Socks': ('socks-001', 'socks-002', 'socks-003', 'socks-004'),
        'Hat': ('hat-001', 'hat-002'),
    }
    return JsonResponse({"result": doc[item]})


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
                    quantity_check = Product.objects.filter(name=product).values()
                    if (quantity_check.first()['stock_quantity'] - quantity) < 0:
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

