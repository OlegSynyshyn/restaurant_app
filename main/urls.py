from django.urls import path
from . import views

urlpatterns = [

    path("", views.home, name="home"),
    path("cart/add/<int:dish_id>/", views.cart_add, name="cart_add"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/update/<int:item_id>/", views.cart_update, name="cart_update"),
    path("cart/remove/<int:item_id>/", views.cart_remove, name="cart_remove"),
]