from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    slug = models.SlugField(max_length=120, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"


class Dish(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва страви")
    slug = models.SlugField(max_length=220, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    ingredients = models.TextField(blank=True, null=True, verbose_name="Інгредієнти")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to="dishes/", blank=True, null=True, verbose_name="Фото")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="dishes", verbose_name="Категорія")
    is_available = models.BooleanField(default=True, verbose_name="В наявності")
    is_popular = models.BooleanField(default=False, verbose_name="Популярне")
    is_new = models.BooleanField(default=False, verbose_name="Нове")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Додано")

    def __str__(self):
        return f"{self.name} — {self.price} ₴"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Страва"
        verbose_name_plural = "Страви"


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                             related_name="carts", verbose_name="Користувач")
    session_key = models.CharField(max_length=40, blank=True, null=True, verbose_name="Сесія гостя")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")
    is_active = models.BooleanField(default=True, verbose_name="Активний")

    def __str__(self):
        if self.user:
            return f"Кошик {self.user.username}"
        return "Кошик гостя"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    class Meta:
        verbose_name = "Кошик"
        verbose_name_plural = "Кошики"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Кошик")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="cart_items", verbose_name="Страва")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return f"{self.dish.name} × {self.quantity}"

    def get_total_price(self):
        return self.dish.price * self.quantity

    class Meta:
        verbose_name = "Позиція в кошику"
        verbose_name_plural = "Позиції в кошику"


class Order(models.Model):
    PAYMENT_CHOICES = [
        ("cash", "Готівка"),
        ("online", "Онлайн-оплата"),
    ]

    STATUS_CHOICES = [
        ("new", "Нове"),
        ("in_progress", "Готується"),
        ("delivering", "Доставляється"),
        ("completed", "Виконане"),
        ("canceled", "Скасоване"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="orders", verbose_name="Користувач")
    customer_name = models.CharField(max_length=150, verbose_name="Ім'я замовника")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    delivery_address = models.TextField(verbose_name="Адреса доставки")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default="cash", verbose_name="Оплата")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус")
    comment = models.TextField(blank=True, null=True, verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return f"Замовлення #{self.id}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Замовлення")
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT, related_name="order_items", verbose_name="Страва")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна на момент замовлення")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return f"{self.dish.name} × {self.quantity}"

    def get_total_price(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = "Позиція замовлення"
        verbose_name_plural = "Позиції замовлення"


class Review(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="reviews", verbose_name="Страва")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews",
                             verbose_name="Користувач")
    rating = models.PositiveSmallIntegerField(default=5, verbose_name="Рейтинг")
    text = models.TextField(blank=True, null=True, verbose_name="Текст відгуку")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата додавання")
    is_approved = models.BooleanField(default=False, verbose_name="Схвалено")

    def __str__(self):
        return f"{self.user} → {self.dish} ({self.rating}/5)"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
