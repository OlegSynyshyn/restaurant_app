from django.contrib import admin
from .models import Category, Dish, Cart, CartItem, Order, OrderItem, Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_available", "is_popular", "is_new")
    list_filter = ("category", "is_available", "is_popular", "is_new")
    search_fields = ("name", "ingredients")
    list_editable = ("price", "is_available", "is_popular", "is_new")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("category", "name")


admin.site.register(Category, CategoryAdmin)
admin.site.register(Dish, DishAdmin)

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
