import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_receipt_pdf(order):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # Encabezado
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Recibo de Compra - Tenis with Rodry")
    
    c.setFont("Helvetica", 12)
    c.drawString(100, 730, f"Orden: {order.ticket_number}")
    c.drawString(100, 710, f"Cliente: {order.user.first_name} {order.user.last_name} ({order.user.email})")
    
    y = 670
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, y, "Productos:")
    c.setFont("Helvetica", 12)
    y -= 20
    
    for item in order.items.all():
        product_name = item.product_name_snapshot if item.product_name_snapshot else item.product.name
        c.drawString(120, y, f"- {product_name}")
        c.drawString(400, y, f"Cant: {item.quantity}")
        c.drawString(480, y, f"${item.price_at_purchase}")
        y -= 20
    
    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, f"Total Pagado: ${order.total_amount}")
    
    y -= 40
    c.setFont("Helvetica", 12)
    c.drawString(100, y, "¡Gracias por tu compra!")
    c.drawString(100, y - 20, "El pedido será despachado dentro de 24 horas.")
    
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
