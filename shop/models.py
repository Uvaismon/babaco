from django.db import models
from PIL import Image


class Store(models.Model):
    objects = None
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, null=False)
    location = models.TextField(null=False)
    contact = models.BigIntegerField(blank=True, null=True)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=256, null=False)


class Customer(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, null=False)
    email = models.EmailField(null=False, unique=True)
    password = models.CharField(max_length=256, null=False)


class Product(models.Model):
    objects = None
    prod_id = models.AutoField(primary_key=True)
    store_id = models.ForeignKey('Store', on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=32, null=False)
    details = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=7)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_pics/')
    deliverable = models.BooleanField(default=False)
    imageUrl = models.CharField(max_length=512, null=True, blank=True)


class Review(models.Model):
    rev_id = models.AutoField(primary_key=True)
    prod_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    cust_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(null=False)
    remarks = models.TextField()
    date = models.DateField()


class Order(models.Model):
    objects = None
    order_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey('Customer', on_delete=models.SET_NULL, null=True)
    prod_id = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    date = models.DateField(null=False)
    delivered = models.BooleanField(null=False, default=False)
    address = models.TextField(null=False)
    quantity = models.IntegerField(default=1)


class Category(models.Model):
    cat_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name
