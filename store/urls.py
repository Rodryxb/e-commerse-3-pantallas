from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('switch_store/<str:store_name>/', views.switch_store, name='switch_store'),
    path('productos/todos/', views.catalogo_todos, name='catalogo_todos'),
    path('productos/<str:category>/', views.catalogo, name='catalogo'),
    path('producto/<int:product_id>/', views.producto_detalle, name='producto_detalle'),
    path('cuenta/', views.cuenta, name='cuenta'),
    path('carrito/', views.carrito, name='carrito'),
    path('carrito/eliminar/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('checkout/', views.checkout, name='checkout'),
    path('ranking/', views.ranking, name='ranking'),
    path('panel/pagos/', views.gestion_pagos, name='gestion_pagos'),
    path('panel/reporte-stock/', views.reporte_stock, name='reporte_stock'),
    path('producto/nuevo/', views.ProductCreateView.as_view(), name='product_create'),
    path('producto/<int:pk>/editar/', views.ProductUpdateView.as_view(), name='product_update'),
    path('producto/<int:pk>/eliminar/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('categoria/<int:pk>/editar/', views.CategoryCardUpdateView.as_view(), name='category_update'),
    path('checkout/exito/<str:ticket_number>/', views.checkout_exito, name='checkout_exito'),
    path('registro/', views.registro, name='registro'),
    path('review/eliminar/<int:review_id>/', views.eliminar_review, name='eliminar_review'),
    path('destacados/agregar/', views.featured_add, name='featured_add'),
    path('destacados/quitar/<int:featured_id>/', views.featured_remove, name='featured_remove'),
    path('destacados/buscar/', views.featured_search, name='featured_search'),
]
