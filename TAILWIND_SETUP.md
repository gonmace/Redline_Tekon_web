# Configuración de Tailwind CSS con Django

## ✅ Configuración Completada

Se ha configurado exitosamente Tailwind CSS v4.1.16 (última versión) con DaisyUI v5.3.10 usando la librería `django-tailwind`, eliminando la instalación separada de Node.js y archivos CSS conflictivos.

## 📁 Estructura de Archivos

```
tekonRL/
├── theme/                          # App de Tailwind CSS
│   ├── static_src/
│   │   ├── src/styles.css         # Archivo principal con configuración @theme
│   │   └── package.json           # Dependencias de Node.js (solo para Tailwind)
│   └── static/css/dist/
│       └── styles.css             # CSS compilado
├── start_tailwind_dev.sh          # Script para modo desarrollo
└── tekon_website/settings.py      # Configuración de Django actualizada
```

**Nota**: En Tailwind v4, ya no se usa `tailwind.config.js`. La configuración se hace directamente en el archivo CSS usando `@theme`.

## 🎨 Colores Personalizados Configurados

- `tekon-red`: #DC2626
- `tekon-red-dark`: #B91C1C
- `tekon-black`: #111827
- `tekon-gray`: #6B7280
- `inter`: Fuente Inter configurada

## 🌼 DaisyUI v5.3.10

DaisyUI es un framework de componentes que funciona perfectamente con Tailwind CSS, proporcionando componentes pre-construidos y temas listos para usar.

### Componentes Disponibles:
- **Botones**: `btn`, `btn-primary`, `btn-secondary`, etc.
- **Cards**: `card`, `card-body`, `card-title`, etc.
- **Formularios**: `input`, `textarea`, `select`, `checkbox`, etc.
- **Alertas**: `alert`, `alert-info`, `alert-success`, etc.
- **Navegación**: `navbar`, `menu`, `tabs`, etc.
- **Layout**: `hero`, `stats`, `divider`, etc.
- **Y muchos más...**

### Demo de Componentes:
Visita `http://localhost:8000/demo-daisyui/` para ver todos los componentes en acción.

## 🏗️ Diseño Moderno para Empresa Constructora

Se ha implementado un diseño profesional y moderno específicamente diseñado para empresas constructoras, con una paleta de colores corporativa y componentes optimizados.

### Características del Diseño:
- **Navegación moderna**: Con efectos de hover y transiciones suaves
- **Hero sections**: Con gradientes y estadísticas destacadas
- **Cards profesionales**: Con sombras y efectos de hover
- **Botones personalizados**: Con estilos corporativos
- **Footer completo**: Con información de contacto y redes sociales
- **Responsive design**: Optimizado para todos los dispositivos

### Paleta de Colores Corporativa:
- **Primarios**: Rojo TEKON (#DC2626), Azul corporativo (#1E40AF), Naranja acento (#EA580C)
- **Neutros**: Negro profesional (#0F172A), Grises escalados
- **Estados**: Verde éxito, Amarillo advertencia, Rojo error

### Componentes Personalizados:
- `.btn-tekon-primary` - Botón principal corporativo
- `.btn-tekon-secondary` - Botón secundario
- `.card-tekon` - Cards profesionales
- `.service-card` - Cards de servicios
- `.stat-tekon` - Estadísticas destacadas
- `.nav-tekon` - Navegación moderna
- `.hero-tekon` - Secciones hero con gradientes

### Demo del Diseño:
Visita `http://localhost:8000/demo-moderno/` para ver el diseño completo en acción.

## 🆕 Nueva Sintaxis de Tailwind v4

En Tailwind v4, la configuración se hace directamente en el archivo CSS usando `@theme`:

```css
@theme {
  --color-tekon-red: #DC2626;
  --color-tekon-red-dark: #B91C1C;
  --color-tekon-black: #111827;
  --color-tekon-gray: #6B7280;
  
  --font-family-inter: 'Inter', sans-serif;
  
  --breakpoint-xs: 475px;
}

/* Configuración de DaisyUI */
@plugin "daisyui";
```

**Ventajas de la nueva sintaxis:**
- ✅ Configuración más simple y directa
- ✅ No necesita archivo `tailwind.config.js` separado
- ✅ Variables CSS nativas para mejor rendimiento
- ✅ Mejor integración con herramientas de desarrollo

## 🚀 Comandos Disponibles

### Desarrollo
```bash
# Iniciar servidor Django
python manage.py runserver

# Iniciar modo desarrollo de Tailwind (watch mode)
python manage.py tailwind start
# o usar el script
./start_tailwind_dev.sh
```

### Producción
```bash
# Compilar CSS para producción
python manage.py tailwind build
```

## 🧪 Prueba de Configuración

**Prueba la configuración:**
- **Tailwind CSS**: `http://localhost:8000/test-tailwind/` - Colores personalizados y utilidades
- **DaisyUI**: `http://localhost:8000/demo-daisyui/` - Componentes pre-construidos
- **Diseño Moderno**: `http://localhost:8000/demo-moderno/` - Diseño profesional para empresa constructora

## 📝 Uso en Templates

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/dist/styles.css' %}">

<!-- Usar colores personalizados -->
<div class="bg-tekon-red text-white p-4">
    <h1 class="text-tekon-black">Título</h1>
    <p class="text-tekon-gray">Descripción</p>
</div>
```

## ⚙️ Configuración en settings.py

```python
INSTALLED_APPS = [
    # ... otras apps
    'tailwind',
    'theme',
    # ... otras apps
]

# Configuración de Tailwind
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = [
    "127.0.0.1",
]
```

## 🔄 Flujo de Trabajo

1. **Desarrollo**: Usar `python manage.py tailwind start` para modo watch
2. **Editar estilos**: Modificar `theme/static_src/src/styles.css`
3. **Configurar Tailwind**: Editar la sección `@theme` en `theme/static_src/src/styles.css`
4. **Producción**: Ejecutar `python manage.py tailwind build` antes de deploy

## ✨ Ventajas de esta Configuración

- ✅ **Tailwind CSS v4.1.16** (última versión disponible)
- ✅ **Sin instalación separada de Node.js** en el proyecto
- ✅ **Integración completa con Django** usando django-tailwind
- ✅ **Colores corporativos de TEKON** preconfigurados
- ✅ **Modo desarrollo** con watch automático
- ✅ **Compilación optimizada** para producción
- ✅ **Configuración limpia** sin archivos CSS conflictivos

## 🔧 Solución de Problemas

### Problema: "Cannot apply unknown utility class"
**Solución**: Eliminar archivos CSS conflictivos que definen clases personalizadas manualmente. Tailwind v4 maneja los colores personalizados a través del archivo `tailwind.config.js`.

### Archivos eliminados:
- `empresa/static/empresa/css/input.css`
- `empresa/static/empresa/css/style.css`
- `staticfiles/empresa/css/` (directorio completo)
