import csv
import datetime
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from .models import Product, Order, OrderItem, Cart, CartItem, AtpRanking

def index(request):
    from .models import CategoryCard, StoreReview
    from .forms import StoreReviewForm
    
    cards = CategoryCard.objects.all()
    reviews = StoreReview.objects.all()
    
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        form = StoreReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, '¡Gracias por tu reseña!')
            return redirect('index')
    else:
        form = StoreReviewForm()
        
    return render(request, 'store/index.html', {
        'cards': cards, 
        'reviews': reviews, 
        'review_form': form
    })

def catalogo(request, category):
    products = Product.objects.filter(category=category, is_active=True)
    
    sort = request.GET.get('sort')
    if sort == 'precio_asc':
        products = products.order_by('price')
    elif sort == 'precio_desc':
        products = products.order_by('-price')
        
    return render(request, 'store/catalogo.html', {
        'products': products, 
        'category': category,
        'current_sort': sort
    })

def catalogo_todos(request):
    products = Product.objects.filter(is_active=True)
    
    q = request.GET.get('q')
    if q:
        products = products.filter(name__icontains=q)
    
    sort = request.GET.get('sort')
    if sort == 'precio_asc':
        products = products.order_by('price')
    elif sort == 'precio_desc':
        products = products.order_by('-price')
        
    category_title = f'Resultados para "{q}"' if q else 'Todos los Productos'
        
    return render(request, 'store/catalogo.html', {
        'products': products, 
        'category': category_title,
        'current_sort': sort,
        'current_q': q
    })

@login_required(login_url='/login/?error=Sin cuenta activa, no hay carrito')
def carrito(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})
            if not created:
                if cart_item.quantity < product.stock:
                    cart_item.quantity += 1
                    cart_item.save()
            messages.success(request, f"{product.name} añadido al carrito.")
            return redirect('carrito')
            
    total = sum((item.product.discount_price or item.product.price) * item.quantity for item in cart.items.all())
            
    return render(request, 'store/carrito.html', {'cart': cart, 'total': total})

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()
    if not items.exists():
        return redirect('carrito')

    try:
        with transaction.atomic():
            # Bloqueo removido por compatibilidad con SQLite local
            product_ids = items.values_list('product_id', flat=True)
            products = Product.objects.filter(id__in=product_ids)
            
            product_map = {p.id: p for p in products}
            
            total_amount = 0
            for item in items:
                p = product_map[item.product_id]
                if p.stock < item.quantity:
                    raise Exception(f"Stock insuficiente para {p.name}")
                p.stock -= item.quantity
                p.save()
                
                price = p.discount_price if p.discount_price else p.price
                total_amount += price * item.quantity
                
            order = Order.objects.create(
                ticket_number=str(uuid.uuid4().hex)[:10].upper(),
                user=request.user,
                status='Esperando aprobacion',
                total_amount=total_amount,
                region_chile='RM',
                comuna_chile='Santiago'
            )
            
            for item in items:
                p = product_map[item.product_id]
                price = p.discount_price if p.discount_price else p.price
                OrderItem.objects.create(
                    order=order,
                    product=p,
                    product_name_snapshot=p.name,
                    quantity=item.quantity,
                    price_at_purchase=price
                )
            
            cart.items.all().delete()
            # Redirect to the new success page instead of cuenta
            return redirect('checkout_exito', ticket_number=order.ticket_number)
            
    except Exception as e:
        messages.error(request, str(e))
        return redirect('carrito')

@login_required
def cuenta(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/cuenta.html', {'orders': orders})

def ranking(request):
    rankings = AtpRanking.objects.all().order_by('rank')
    now = timezone.now()
    days_ahead = 0 - now.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    next_monday = now + datetime.timedelta(days=days_ahead)
    next_monday = next_monday.replace(hour=0, minute=0, second=0, microsecond=0)
    timestamp = int(next_monday.timestamp() * 1000)
    return render(request, 'store/ranking.html', {'rankings': rankings, 'target_timestamp': timestamp})

@staff_member_required
def reporte_stock(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig') # utf-8-sig para tildes en Excel
    response['Content-Disposition'] = 'attachment; filename="inventario_reporte.csv"'
    writer = csv.writer(response, delimiter=';') # punto y coma es mejor para Excel en español
    
    # Cabeceras mejoradas
    writer.writerow(['SKU', 'Nombre', 'Categoría', 'Precio Unitario', 'Stock Actual', 'Estado', 'Valorizado en Bodega'])
    
    for p in Product.objects.all().order_by('stock'):
        estado = "Agotado" if p.stock == 0 else "Disponible"
        valor_bodega = p.stock * p.price
        writer.writerow([
            p.sku, 
            p.name, 
            p.category.capitalize(), 
            f"${p.price}", 
            p.stock, 
            estado, 
            f"${valor_bodega}"
        ])
        
    return response

def handler404(request, exception):
    return render(request, '404.html', status=404)

def handler500(request):
    return render(request, '500.html', status=500)


from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import ProductForm

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class ProductCreateView(StaffRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    def get_success_url(self):
        return reverse_lazy('catalogo', kwargs={'category': self.object.category})

class ProductUpdateView(StaffRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'store/product_form.html'
    def get_success_url(self):
        return reverse_lazy('catalogo', kwargs={'category': self.object.category})

class ProductDeleteView(StaffRequiredMixin, DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('index')

@login_required
def eliminar_del_carrito(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    product_name = item.product.name
    item.delete()
    messages.success(request, f'"{product_name}" ha sido eliminado del carrito.')
    return redirect('carrito')


from django.contrib.auth import login
from .forms import UserRegistrationForm

def registro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso! Bienvenido a Tenis with Rodry.')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'store/registro.html', {'form': form})

@login_required
def checkout_exito(request, ticket_number):
    order = get_object_or_404(Order, ticket_number=ticket_number, user=request.user)
    return render(request, 'store/checkout_exito.html', {'order': order})


from .models import CategoryCard
from .forms import CategoryCardForm

class CategoryCardUpdateView(StaffRequiredMixin, UpdateView):
    model = CategoryCard
    form_class = CategoryCardForm
    template_name = 'store/category_form.html'
    success_url = reverse_lazy('index')


from django.core.mail import EmailMessage
from .utils import generate_receipt_pdf

@staff_member_required
def gestion_pagos(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        action = request.POST.get('action')
        order = get_object_or_404(Order, id=order_id)
        if action == 'recibido':
            order.status = 'Pago recibido'
            order.save()
            messages.success(request, f'Orden {order.ticket_number} marcada como PAGO RECIBIDO.')
            
            try:
                # Generar PDF Nivel Dios
                pdf_content = generate_receipt_pdf(order)
                
                # Enviar correo
                email = EmailMessage(
                    subject=f'Pago Confirmado - Orden {order.ticket_number} - Tenis with Rodry',
                    body=f'¡Hola {order.user.first_name}!\n\nHemos verificado tu transferencia exitosamente.\n\nEl pedido será despachado dentro de 24 horas.\n\nAdjuntamos la boleta oficial de tu compra.\n\nSaludos,\nEquipo Tenis with Rodry.',
                    from_email='ventas@teniswithrodry.cl',
                    to=[order.user.email],
                )
                email.attach(f'Boleta_{order.ticket_number}.pdf', pdf_content, 'application/pdf')
                email.send(fail_silently=False)
                messages.success(request, f'Correo con boleta PDF enviado a {order.user.email}.')
            except Exception as e:
                messages.error(request, f'Pago aprobado, pero hubo un error enviando el correo: {e}')
                
        elif action == 'no_recibido':
            order.status = 'Pago no recibido'
            order.save()
            messages.error(request, f'Orden {order.ticket_number} marcada como PAGO NO RECIBIDO.')
        return redirect('gestion_pagos')
        
    orders = Order.objects.filter(status='Esperando aprobacion').order_by('created_at')
    return render(request, 'store/gestion_pagos.html', {'orders': orders})
