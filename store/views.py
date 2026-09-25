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
    from .models import CategoryCard, StoreReview, FeaturedProduct
    from .forms import StoreReviewForm
    
    active_store = request.session.get('active_store', 'tenis')
    cards = CategoryCard.objects.filter(store=active_store)
    reviews = StoreReview.objects.all()
    featured_products = list(FeaturedProduct.objects.filter(store=active_store).select_related('product')[:5])
    
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
        'review_form': form,
        'featured_products': featured_products,
    })

import requests

def catalogo(request, category):
    products = Product.objects.filter(category=category, is_active=True)
    
    sort = request.GET.get('sort')
    if sort == 'precio_asc':
        products = products.order_by('price')
    elif sort == 'precio_desc':
        products = products.order_by('-price')
        
    standings = None
    if category == 'tabla_a':
        try:
            # Pega aquí tu API Key de api-sports.io
            api_key = 'TU_API_KEY_AQUI'
            headers = {
                'x-rapidapi-key': api_key,
                'x-rapidapi-host': 'v3.football.api-sports.io'
            }
            # 265 es la Liga Chilena Primera División
            response = requests.get('https://v3.football.api-sports.io/standings?league=265&season=2024', headers=headers, timeout=3)
            
            if response.status_code == 200 and 'response' in response.json() and len(response.json()['response']) > 0:
                standings = response.json()['response'][0]['league']['standings'][0]
            else:
                raise Exception("API Auth failed")
        except:
            # Fallback exacto con los 16 equipos de primera division 2024 si no hay API key
            standings = [
                {'rank': 1, 'team': {'name': 'Colo Colo', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/4/4f/Escudo_del_Club_Social_y_Deportivo_Colo-Colo.png'}, 'points': 54, 'all': {'played': 23, 'win': 17, 'draw': 3, 'lose': 3, 'goals': {'for': 48, 'against': 22}}, 'goalsDiff': 26},
                {'rank': 2, 'team': {'name': 'Universidad Católica', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/c/c5/Escudo_de_Cruzados_SADP.svg'}, 'points': 42, 'all': {'played': 23, 'win': 13, 'draw': 3, 'lose': 7, 'goals': {'for': 50, 'against': 33}}, 'goalsDiff': 17},
                {'rank': 3, 'team': {'name': 'Universidad de Chile', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/3/30/Escudo_del_Club_Universidad_de_Chile.svg'}, 'points': 42, 'all': {'played': 23, 'win': 12, 'draw': 6, 'lose': 5, 'goals': {'for': 35, 'against': 19}}, 'goalsDiff': 16},
                {'rank': 4, 'team': {'name': 'Everton CD', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/f/fb/Escudo_de_Everton_de_Vi%C3%B1a_del_Mar.svg'}, 'points': 36, 'all': {'played': 23, 'win': 10, 'draw': 6, 'lose': 7, 'goals': {'for': 37, 'against': 25}}, 'goalsDiff': 12},
                {'rank': 5, 'team': {'name': 'Palestino', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/5/5a/Escudo_del_Club_Deportivo_Palestino.svg'}, 'points': 36, 'all': {'played': 23, 'win': 11, 'draw': 3, 'lose': 9, 'goals': {'for': 36, 'against': 33}}, 'goalsDiff': 3},
                {'rank': 6, 'team': {'name': 'Deportes Limache', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/4/4e/Deportes_Limache.png'}, 'points': 33, 'all': {'played': 23, 'win': 10, 'draw': 3, 'lose': 10, 'goals': {'for': 43, 'against': 35}}, 'goalsDiff': 8},
                {'rank': 7, 'team': {'name': 'Ñublense', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/4/4d/Escudo_del_Club_Deportivo_%C3%91ublense.svg'}, 'points': 32, 'all': {'played': 23, 'win': 8, 'draw': 8, 'lose': 7, 'goals': {'for': 28, 'against': 31}}, 'goalsDiff': -3},
                {'rank': 8, 'team': {'name': 'Deportes Concepcion', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/5/57/Escudo_de_Deportes_Concepci%C3%B3n.svg'}, 'points': 31, 'all': {'played': 23, 'win': 9, 'draw': 4, 'lose': 10, 'goals': {'for': 25, 'against': 26}}, 'goalsDiff': -1},
                {'rank': 9, 'team': {'name': 'La Serena', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/3/39/Escudo_de_Deportes_La_Serena.svg'}, 'points': 30, 'all': {'played': 23, 'win': 7, 'draw': 9, 'lose': 7, 'goals': {'for': 34, 'against': 38}}, 'goalsDiff': -4},
                {'rank': 10, 'team': {'name': 'Coquimbo Unido', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/1/1b/Escudo_de_Coquimbo_Unido.svg'}, 'points': 29, 'all': {'played': 23, 'win': 8, 'draw': 5, 'lose': 10, 'goals': {'for': 31, 'against': 32}}, 'goalsDiff': -1},
                {'rank': 11, 'team': {'name': 'Audax Italiano', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/1/1a/Escudo_de_Audax_Italiano.svg'}, 'points': 28, 'all': {'played': 23, 'win': 7, 'draw': 7, 'lose': 9, 'goals': {'for': 26, 'against': 31}}, 'goalsDiff': -5},
                {'rank': 12, 'team': {'name': 'Huachipato', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/8/87/Escudo_del_Club_Deportivo_Huachipato.svg'}, 'points': 28, 'all': {'played': 22, 'win': 8, 'draw': 4, 'lose': 10, 'goals': {'for': 30, 'against': 39}}, 'goalsDiff': -9},
                {'rank': 13, 'team': {'name': "O'Higgins", 'logo': 'https://upload.wikimedia.org/wikipedia/commons/3/3b/Escudo_de_O%27Higgins_de_Rancagua.svg'}, 'points': 27, 'all': {'played': 23, 'win': 8, 'draw': 3, 'lose': 12, 'goals': {'for': 28, 'against': 36}}, 'goalsDiff': -8},
                {'rank': 14, 'team': {'name': 'Cobresal', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/4/49/Escudo_de_Club_de_Deportes_Cobresal.svg'}, 'points': 24, 'all': {'played': 23, 'win': 7, 'draw': 3, 'lose': 13, 'goals': {'for': 34, 'against': 44}}, 'goalsDiff': -10},
                {'rank': 15, 'team': {'name': 'Universidad de Concepcion', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/6/62/Escudo_del_Club_Deportivo_Universidad_de_Concepci%C3%B3n.svg'}, 'points': 22, 'all': {'played': 22, 'win': 6, 'draw': 4, 'lose': 12, 'goals': {'for': 17, 'against': 37}}, 'goalsDiff': -20},
                {'rank': 16, 'team': {'name': 'Unión La Calera', 'logo': 'https://upload.wikimedia.org/wikipedia/commons/9/9f/Escudo_de_Uni%C3%B3n_La_Calera.svg'}, 'points': 17, 'all': {'played': 23, 'win': 4, 'draw': 5, 'lose': 14, 'goals': {'for': 19, 'against': 40}}, 'goalsDiff': -21}
            ]
            
    return render(request, 'store/catalogo.html', {
        'products': products, 
        'category': category,
        'current_sort': sort,
        'standings': standings
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
        quantity = int(request.POST.get('quantity', 1))
        
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            
            # Sum quantity with existing cart item
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()
            current_qty = cart_item.quantity if cart_item else 0
            
            if current_qty + quantity > product.stock:
                messages.error(request, f"No puedes añadir {quantity} de {product.name}. Solo hay {product.stock - current_qty} disponibles más.")
            else:
                if cart_item:
                    cart_item.quantity += quantity
                    cart_item.save()
                else:
                    CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                messages.success(request, f"{quantity}x {product.name} añadido al carrito.")
                
            return redirect(request.META.get('HTTP_REFERER', 'carrito'))
            
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


@staff_member_required
def eliminar_review(request, review_id):
    from .models import StoreReview
    review = get_object_or_404(StoreReview, id=review_id)
    review.delete()
    messages.success(request, 'Reseña eliminada correctamente.')
    return redirect('index')


def producto_detalle(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/producto_detalle.html', {'product': product})

def switch_store(request, store_name):
    request.session['active_store'] = store_name
    return redirect('index')


# --- Gestión de Productos Destacados (solo superusuario) ---
from django.http import JsonResponse

@staff_member_required
def featured_add(request):
    from .models import FeaturedProduct
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        store = request.session.get('active_store', 'tenis')
        product = get_object_or_404(Product, id=product_id)
        count = FeaturedProduct.objects.filter(store=store).count()
        if count >= 5:
            messages.error(request, 'Ya hay 5 productos destacados. Quita uno antes de agregar otro.')
        elif FeaturedProduct.objects.filter(store=store, product=product).exists():
            messages.warning(request, f'"{product.name}" ya está en destacados.')
        else:
            FeaturedProduct.objects.create(store=store, product=product, order=count + 1)
            messages.success(request, f'"{product.name}" agregado a destacados.')
    return redirect('index')

@staff_member_required
def featured_remove(request, featured_id):
    from .models import FeaturedProduct
    fp = get_object_or_404(FeaturedProduct, id=featured_id)
    name = fp.product.name
    fp.delete()
    messages.success(request, f'"{name}" eliminado de destacados.')
    return redirect('index')

@staff_member_required
def featured_search(request):
    q = request.GET.get('q', '')
    store = request.session.get('active_store', 'tenis')
    from .models import FeaturedProduct
    already_ids = FeaturedProduct.objects.filter(store=store).values_list('product_id', flat=True)
    products = Product.objects.filter(name__icontains=q, is_active=True).exclude(id__in=already_ids)[:10]
    data = [{'id': p.id, 'name': p.name, 'price': str(p.price), 'sku': p.sku} for p in products]
    return JsonResponse({'results': data})
