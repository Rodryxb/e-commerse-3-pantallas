from django.contrib import admin
from .models import Product, Order, OrderItem, AtpRanking, FeaturedProduct

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'price', 'stock', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'sku')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('ticket_number', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('ticket_number', 'user__username')

@admin.register(FeaturedProduct)
class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'store', 'product')
    list_display_links = ('product',)
    list_filter = ('store',)
    list_editable = ('order', 'store')
    autocomplete_fields = ['product']
    ordering = ('store', 'order')

admin.site.register(OrderItem)
admin.site.register(AtpRanking)
