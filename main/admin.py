from django.contrib import admin

from main.models import Category, Dish, Order, OrderItem

# Register your models here.

admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Order)
admin.site.register(OrderItem)

