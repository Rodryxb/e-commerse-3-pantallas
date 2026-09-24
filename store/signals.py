from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def return_stock_on_cancel(sender, instance, **kwargs):
    if instance.status == 'Cancelado':
        for item in instance.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
