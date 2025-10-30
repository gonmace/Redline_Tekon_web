# TEKON RedLine - Sitio Web Corporativo

Sitio web corporativo para TEKON RedLine SPA, empresa especializada en ingeniería, construcción y supervisión.

## 🚀 Características

- **Django 4.2+** - Framework web robusto
- **Tailwind CSS v4** - Framework CSS moderno y utilitario
- **DaisyUI 5.3+** - Componentes UI elegantes
- **Diseño Responsivo** - Optimizado para todos los dispositivos
- **Modo Oscuro/Claro** - Temas intercambiables
- **Paleta de Colores TEKON** - Identidad visual corporativa

## 🎨 Paleta de Colores

- **Primario**: Rojo TEKON (`#dc2626`)
- **Secundario**: Verde esmeralda (`#059669` / `#10b981`)
- **Acento**: Naranja (`#ea580c` / `#fb923c`)
- **Neutros**: Grises y blancos para fondos y texto

## 📁 Estructura del Proyecto

```
tekonRL/
├── empresa/                 # App principal de la empresa
│   ├── templates/          # Templates HTML
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas
│   └── urls.py            # URLs
├── theme/                  # App de Tailwind CSS
│   ├── static_src/        # Archivos fuente CSS
│   └── templates/         # Templates de prueba
├── tekon_website/         # Configuración Django
└── static/                # Archivos estáticos compilados
```

## 🛠️ Instalación

### Prerrequisitos

- Python 3.8+
- Node.js (para Tailwind CSS)
- pip

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd tekonRL
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # o
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias Python**
   ```bash
   pip install -r requirements.txt
   ```

4. **Instalar dependencias Node.js**
   ```bash
   cd theme/static_src
   npm install
   cd ../..
   ```

5. **Configurar base de datos**
   ```bash
   python manage.py migrate
   ```

6. **Compilar CSS**
   ```bash
   python manage.py tailwind build
   ```

7. **Ejecutar servidor**
   ```bash
   python manage.py runserver
   ```

## 🎯 Uso

### Desarrollo CSS

Para desarrollo con recarga automática de CSS:

```bash
python manage.py tailwind start
```

### Compilación de Producción

```bash
python manage.py tailwind build
```

### Poblar Base de Datos

```bash
python manage.py shell
>>> exec(open('populate_database.py').read())
```

## 📱 Páginas Disponibles

- **Inicio** (`/`) - Página principal con servicios destacados
- **Sobre Nosotros** (`/sobre-nosotros/`) - Historia y valores de la empresa
- **Servicios** (`/servicios/`) - Catálogo de servicios
- **Proyectos** (`/proyectos/`) - Portafolio de proyectos
- **Equipo** (`/equipo/`) - Información del equipo
- **Clientes** (`/clientes/`) - Clientes y testimonios
- **Contacto** (`/contacto/`) - Formulario de contacto

## 🎨 Personalización

### Colores

Los colores se definen en `theme/static_src/src/styles.css`:

```css
[data-theme="light"] {
  --color-primary: #dc2626;
  --color-secondary: #059669;
  --color-accent: #ea580c;
}
```

### Componentes

Los componentes utilizan clases de DaisyUI y Tailwind CSS:

```html
<div class="card bg-base-100 shadow-lg">
  <div class="card-body">
    <h2 class="card-title text-primary">Título</h2>
    <p class="text-base-content/70">Contenido</p>
  </div>
</div>
```

## 🌙 Modo Oscuro

El sitio incluye modo oscuro automático con persistencia en localStorage:

- **Toggle**: Botón en la navegación
- **Persistencia**: Se recuerda la preferencia del usuario
- **Contraste**: Optimizado para legibilidad

## 📦 Tecnologías

- **Backend**: Django 4.2+
- **Frontend**: Tailwind CSS v4, DaisyUI
- **Base de Datos**: SQLite (desarrollo)
- **Iconos**: Font Awesome 6.4
- **Fuentes**: Inter (Google Fonts)

## 🚀 Despliegue

### Producción

1. Configurar variables de entorno
2. Configurar base de datos de producción
3. Compilar CSS: `python manage.py tailwind build`
4. Recopilar archivos estáticos: `python manage.py collectstatic`
5. Configurar servidor web (Nginx + Gunicorn)

### Docker (Opcional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py tailwind build
CMD ["gunicorn", "tekon_website.wsgi:application"]
```

## 📄 Licencia

© 2024 TEKON RedLine SPA. Todos los derechos reservados.

## 👥 Equipo

- **Desarrollo**: Equipo de desarrollo TEKON
- **Diseño**: Identidad visual corporativa
- **Contenido**: Información empresarial

---

**TEKON RedLine SPA** - Soluciones Eficientes en Ingeniería, Construcción y Supervisión
