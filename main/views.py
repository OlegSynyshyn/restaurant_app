from django.shortcuts import render, redirect
from .models import Category, Dish, Cart, CartItem


def home(request):
    categories = Category.objects.all().order_by("order", "name")
    base_qs = Dish.objects.filter(is_available=True)

    popular_dishes = base_qs.filter(is_popular=True)
    new_dishes = base_qs.filter(is_new=True)

    category_slug = request.GET.get("category")
    selected_category = None
    dishes = base_qs

    if category_slug:
        selected_category = Category.objects.filter(slug=category_slug).first()
        if selected_category:
            dishes = base_qs.filter(category=selected_category)

    return render(request, "main/home.html", {
        "categories": categories,
        "dishes": dishes,
        "popular_dishes": popular_dishes,
        "new_dishes": new_dishes,
        "selected_category": selected_category,
    })


def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            is_active=True,
        )
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(
            session_key=session_key,
            is_active=True,
            user=None,
        )

    return cart


def cart_add(request, dish_id):
    dish = Dish.objects.filter(id=dish_id, is_available=True).first()
    if not dish:
        return redirect("home")

    cart = get_cart(request)

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        item = CartItem.objects.filter(cart=cart, dish=dish).first()
        if item:
            item.quantity += quantity
        else:
            item = CartItem(cart=cart, dish=dish, quantity=quantity)

        item.save()

    return redirect("cart_detail")


def cart_detail(request):
    cart = get_cart(request)
    items = CartItem.objects.filter(cart=cart)
    total = cart.get_total_price()

    return render(request, "main/cart.html", {
        "cart": cart,
        "items": items,
        "total": total,
    })


def cart_update(request, item_id):
    cart = get_cart(request)
    item = CartItem.objects.filter(id=item_id, cart=cart).first()

    if item and request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))

        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

    return redirect("cart_detail")


def cart_remove(request, item_id):
    cart = get_cart(request)
    item = CartItem.objects.filter(id=item_id, cart=cart).first()

    if item and request.method == "POST":
        item.delete()

    return redirect("cart_detail")
