from django.db import models


class Category(models.Model):
    category = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.category


class CategorySize(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.CharField(max_length=20)

    def __str__(self):
        return self.size


class Product(models.Model):
    name = models.CharField(max_length=40, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    size = models.ForeignKey(CategorySize, on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    price = models.BigIntegerField()
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Inbound(models.Model):
    """
    입고 모델입니다.
    상품, 수량, 입고 날짜, 금액 필드를 작성합니다.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)


class Outbound(models.Model):
    """
    출고 모델입니다.
    상품, 수량, 입고 날짜, 금액 필드를 작성합니다.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)





