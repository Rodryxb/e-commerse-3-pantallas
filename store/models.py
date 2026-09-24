from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('raquetas', 'Raquetas'),
        ('pelotas', 'Pelotas'),
        ('zapatillas', 'Zapatillas'),
        ('extras', 'Extras'),
    ]
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sku} - {self.name}"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError(f"La cantidad ({self.quantity}) supera el stock disponible ({self.product.stock}).")

class Order(models.Model):
    STATUS_CHOICES = [
        ('Esperando aprobacion', 'Esperando aprobacion'),
        ('Pago recibido', 'Pago recibido'),
        ('Pago no recibido', 'Pago no recibido'),
        ('Despachado', 'Despachado'),
        ('Cancelado', 'Cancelado'),
    ]
    ticket_number = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Esperando aprobacion', db_index=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    region_chile = models.CharField(max_length=100)
    comuna_chile = models.CharField(max_length=100)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name_snapshot = models.CharField(max_length=200, blank=True)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=0)

class AtpRanking(models.Model):
    rank = models.PositiveIntegerField()
    player_name = models.CharField(max_length=100)
    country = models.CharField(max_length=10)
    points = models.PositiveIntegerField()
    fetched_at = models.DateTimeField(auto_now=True)


class CategoryCard(models.Model):
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

class StoreReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Estrellas") for i in range(1, 6)], default=5)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Reseña de {self.user.username}"
