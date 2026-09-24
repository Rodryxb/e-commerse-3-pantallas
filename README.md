# 🎾 Tenis with Rodry | E-Commerce

**Tenis with Rodry** es una plataforma de E-Commerce completa y profesional desarrollada en **Python (Django)** orientada a la venta de artículos de tenis (raquetas, pelotas, zapatillas y accesorios).

El sistema no solo funciona como un catálogo, sino que cuenta con un sistema robusto de carritos de compra, gestión de usuarios, roles de administrador, y automatización de boletas en PDF enviadas directamente al correo del cliente.

---

## ✨ Características Principales (Features)

* 🛒 **Carrito de Compras Dinámico:** Cálculo en tiempo real de subtotales, detección inteligente de precios con descuento y validación de stock.
* 🔐 **Sistema de Usuarios y Roles:** Registro de clientes y portal de administrador (Superusuario).
* 💳 **Flujo de Checkout y Auditoría:** Los pedidos nacen en estado *"Esperando aprobación"*. El administrador cuenta con un panel especial para verificar las transferencias y aprobar los despachos con un clic.
* 📧 **Generación de PDFs y Correos:** Al aprobarse un pago, el sistema dibuja automáticamente una boleta en PDF (`ReportLab`) y se la envía al cliente por correo electrónico informando el despacho en 24 horas.
* 📊 **Panel de Business Intelligence:** Generación instantánea de reportes CSV exportables para Excel con métricas de inventario (Estado, Stock Crítico, Valorización de Bodega).
* 🏆 **Integración de API Externa:** Conexión en tiempo real a la API de ESPN para mostrar el Ranking ATP actualizado de los mejores tenistas del mundo.
* 🔍 **Buscador Inteligente y Filtros:** Buscador global de productos y filtros de ordenamiento por precio.
* ⭐ **Sistema de Reseñas:** Muro público de reseñas de clientes.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django 5.x
* **Base de Datos:** SQLite (Migrable a PostgreSQL para producción)
* **Frontend:** HTML5, CSS3, Bootstrap 5
* **Librerías Adicionales:** 
  * `ReportLab` (Generación de PDFs)
  * `Requests` (Consumo de APIs externas)
  * `Pillow` (Procesamiento de imágenes)

---

## 🚀 Guía de Instalación (Paso a Paso)

Sigue estos pasos para hacer correr el proyecto localmente en cualquier computador:

### 1. Clonar el Repositorio
Abre tu terminal y descarga el proyecto:
```bash
git clone https://github.com/Rodryxb/tenis_with_rodry.git
cd tenis_with_rodry
```

### 2. Crear un Entorno Virtual
Es una buena práctica encapsular las librerías del proyecto.
* En **Windows**:
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
* En **Mac/Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar las Dependencias
Con el entorno virtual activado, instala todas las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

### 4. Configurar la Base de Datos
Ejecuta las migraciones para construir la estructura de la base de datos:
```bash
python manage.py migrate
```

### 5. Crear un Usuario Administrador (Superuser)
Para poder acceder a los botones exclusivos de administrador (Gestión de Pagos, Descarga de Stock, etc.), crea tu cuenta maestra:
```bash
python manage.py createsuperuser
```
*(Te pedirá un nombre de usuario, correo y contraseña. Ojo: cuando escribes la contraseña en la consola no se ve, pero sí se está escribiendo).*

### 6. Obtener Datos del Ranking ATP (Opcional)
Para que la tabla de ranking no esté vacía, corre nuestro comando personalizado que consulta a la API de ESPN:
```bash
python manage.py importar_ranking
```

### 7. Levantar el Servidor
¡Todo listo! Enciende el motor del proyecto:
```bash
python manage.py runserver
```
Entra a tu navegador web favorito y visita `http://127.0.0.1:8000/`.

---

## 💻 Panel de Administración

Una vez que el servidor esté corriendo, puedes:
1. Iniciar sesión con tu cuenta de administrador en la página normal.
2. Usar los botones amarillos de la barra de navegación para **Revisar Transferencias** o descargar el **Stock en CSV**.
3. O si prefieres la vista de base de datos cruda, ve a `http://127.0.0.1:8000/admin/`.
