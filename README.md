# 🪐 Multiverso E-Commerce | 3 Tiendas en 1
**Tenis with Rodry | Fútbol with Rodry | Mundo Meo Corte**

Este proyecto es una plataforma de E-Commerce avanzada desarrollada en **Python (Django)** que implementa un innovador sistema de "Universos Paralelos". Utilizando un único carrito de compras y una misma base de datos centralizada, la interfaz gráfica de la tienda se transforma por completo (estilos, logos, categorías y productos) dependiendo del "Mundo" en el que el cliente decida adentrarse.

---

## ✨ Nuevas Características del Multiverso

* 🌌 **Motor de Temas (Theme Engine):** Cambio instantáneo de variables CSS y diseño. 
  - **Tenis:** Estilo Índigo Oscuro y Neón Cyan 🎾
  - **Fútbol:** Estilo Verde Cancha y Lima Neón ⚽
  - **Meo Corte:** Estilo Dark Clásico y Oro (Dorado) 💎
* 🎛️ **Portales Flotantes Globales:** Una torre lateral "efecto espejo" anclada a la derecha de la pantalla que permite al usuario saltar de un universo a otro con un solo clic, de forma simétrica.
* ⭐ **Vitrina de Destacados Interactiva:** Un carrusel de productos rotativos en la página principal con **efecto fade-in y temporizador (barra de progreso)**. 
* 🛠️ **Panel CRUD en Vivo (Superusuario):** El administrador puede agregar, buscar con autocompletado y eliminar los productos destacados directamente desde la página de inicio, sin entrar al backend de Django.
* 🏆 **Estadísticas y Tablas:**
  - Integración del ranking ATP en tiempo real para el mundo Tenis.
  - Tabla de posiciones exacta de la Primera División Chilena (Campeonato Nacional) para el mundo Fútbol.
* 🛒 **Carrito Global:** Puedes añadir unas zapatillas de Tenis, una pelota de Fútbol y un Reloj de Meo Corte; todo viaja en el mismo carrito para un checkout unificado.
* 📧 **Generación de PDFs y Correos:** Al aprobar un pedido (transferencia), el sistema emite una boleta dinámica vía `ReportLab` y se envía automáticamente al correo del cliente.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django 5.x
* **Base de Datos:** SQLite (Preparado para PostgreSQL)
* **Frontend:** HTML5, CSS3, Bootstrap 5 + JS Vanilla (Animaciones)
* **Librerías Extra:** `ReportLab`, `Requests`, `Pillow`

---

## 🚀 Guía de Instalación Rápida

Sigue estos pasos para arrancar el Multiverso en tu computador:

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Rodryxb/e-commerse-3-pantallas.git
cd tenis_with_rodry
```

### 2. Crear y Activar Entorno Virtual
* **En Windows (PowerShell/CMD):**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```
* **En Mac/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Construir Base de Datos y Poblar
```bash
python manage.py migrate
```

### 5. Crear el Administrador del Multiverso (Superuser)
Obligatorio para que puedas ver el panel interactivo de productos destacados en la pantalla principal:
```bash
python manage.py createsuperuser
```

### 6. Obtener Ranking de Tenis (Opcional)
```bash
python manage.py importar_ranking
```

### 7. Levantar Servidor
```bash
python manage.py runserver
```
Entra a `http://127.0.0.1:8000/` y navega entre los tres mundos usando la torre de portales a la derecha.

---

## 💻 Panel de Administración y Funciones Clave

* **Vitrina en Vivo:** Inicia sesión con la cuenta de superusuario y ve al inicio (`/`). Verás el panel **"Gestionar Productos Destacados"**. Busca productos en el input y agrégalos para armar la vitrina (hasta 5 por universo).
* **Gestión de Pagos:** Botón amarillo en la barra superior (solo superusuario) para auditar ventas, descargar PDFs y aprobar despachos.
* **Descarga de Stock:** Reporte instantáneo de inventario en archivo Excel/CSV.
