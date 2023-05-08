from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

from account.models import User


class ItemsModel(models.Model):
    customer = models.CharField(max_length=50, null= True)
    productName = models.CharField(max_length=50)
    productPrice = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.productName}'

class UserTable(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tableName = models.CharField(max_length=50)
    dateOfCreating = models.DateField(auto_now=True, null=True)
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        ordering = ["-timeOfCreating"]
    
    def __str__(self):
        return self.tableName

class TableItem(models.Model):
    table = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50)
    product_count = models.IntegerField(null=True)
    product_price = models.IntegerField(null=True)
    total_price = models.IntegerField(null=True,default=0)

class BigTable(models.Model):
    table = models.ForeignKey(UserTable, on_delete=models.SET_NULL, null = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null = True)

    def __str__(self) -> str:
        return f'{self.user}'


class Debt(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    debt = models.FloatField()
    timeOfCreating = models.DateTimeField(auto_now=True, null=True)


    class Meta:
        ordering = ["-timeOfCreating"]

    def __str__(self) -> str:
        return f'{self.customer} - {self.debt}'