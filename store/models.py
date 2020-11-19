from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=32)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    #price = models.IntegerField()
    category = models.CharField(max_length=100)






