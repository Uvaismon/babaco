from django.contrib import admin

from shop.models import Product, Customer, Review, Store, Order, Category

admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Review)
admin.site.register(Store)
admin.site.register(Order)
admin.site.register(Category)
