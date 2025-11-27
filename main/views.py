from django.shortcuts import render
from .models import Category, Dish

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
