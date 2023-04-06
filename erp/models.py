from django.db import models


# Create your models here.
class Product(models.Model):

    categorys = (
        ('Jean', 'Jean'),
        ('Hood', 'Hood'),
        ('Socks', 'Socks'),
        ('Hat', 'Hat'),
    )

    name = models.CharField(max_length=40)
    category = models.CharField(choices=categorys, max_length=10)
    code = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    description = models.CharField(max_length=256)
    price = models.BigIntegerField()
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.stock_quantity = 0
        super().save(*args, **kwargs)


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





