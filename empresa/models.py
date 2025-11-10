from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class Empresa(models.Model):
    """Modelo para la información principal de la empresa"""
    nombre = models.CharField(max_length=200, default="TK REDLINE SPA")
    slogan = models.CharField(max_length=200, default="SOLUCIONES EFICIENTES")
    descripcion = models.TextField(blank=True)
    mision = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    valores = models.TextField(blank=True)
    direccion = models.CharField(max_length=300, default="C. Carlos Antúnez 2025, Piso 9-904 – PROVIDENCIA – Santiago de Chile")
    telefono = models.CharField(max_length=20, default="+56 9 3494 9214")
    email_principal = models.EmailField(default="mlujan@tekon-rl.cl")
    email_secundario = models.EmailField(blank=True, null=True)
    imagen_principal = models.ImageField(upload_to='empresa/', blank=True, null=True)
    imagen_fondo_hero = models.ImageField(upload_to='empresa/', blank=True, null=True, 
                                        help_text="Imagen de fondo para la sección hero de la página principal")
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresa"

    def __str__(self):
        return self.nombre

class Servicio(models.Model):
    """Modelo para los servicios de la empresa"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    icono = models.FileField(
        upload_to='servicios/icons/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['svg'])],
        help_text="Archivo SVG del icono del servicio"
    )
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Servicio"
        verbose_name_plural = "Servicios"
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

class Proyecto(models.Model):
    """Modelo para los proyectos destacados"""
    nombre = models.CharField(max_length=300)
    descripcion = models.TextField()
    cliente = models.CharField(max_length=200)
    cliente_rel = models.ForeignKey(
        'Cliente',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proyectos',
        verbose_name='Cliente (lista)'
    )
    alcance = models.TextField()
    imagen = models.ImageField(upload_to='proyectos/', blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"
        ordering = ['orden', '-fecha_creacion']

    def __str__(self):
        return self.nombre

    @property
    def cliente_mostrado(self):
        if self.cliente_rel:
            return self.cliente_rel.nombre
        return self.cliente

class Cliente(models.Model):
    """Modelo para los clientes de la empresa"""
    nombre = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='clientes/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    tipo_cliente = models.CharField(
        max_length=20,
        choices=[
            ('directo', 'Cliente Directo'),
            ('final', 'Cliente Final'),
        ],
        default='directo'
    )
    activo = models.BooleanField(default=True)
    destacado = models.BooleanField(
        default=False,
        help_text="Marcar si el cliente debe aparecer en listados destacados o selecciones."
    )
    orden = models.PositiveIntegerField(default=0)
    puntos_importantes = models.TextField(
        blank=True,
        help_text="Listado opcional (separado por saltos de línea) de hitos a mostrar en clientes destacados."
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre

    @property
    def puntos_importantes_list(self):
        if not self.puntos_importantes:
            return []
        return [punto.strip() for punto in self.puntos_importantes.splitlines() if punto.strip()]

class Equipo(models.Model):
    """Modelo para el equipo de la empresa"""
    nombre = models.CharField(max_length=200)
    cargo = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='equipo/', blank=True, null=True)
    descripcion = models.TextField(blank=True)
    socio = models.BooleanField(default=False, verbose_name="Socio")
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Miembro del Equipo"
        verbose_name_plural = "Equipo"
        ordering = ['orden', 'nombre']

    def __str__(self):
        return f"{self.nombre} - {self.cargo}"

class Contacto(models.Model):
    """Modelo para mensajes de contacto"""
    nombre = models.CharField(max_length=200)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True)
    empresa = models.CharField(max_length=200, blank=True)
    asunto = models.CharField(max_length=300)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    respondido = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Mensaje de Contacto"
        verbose_name_plural = "Mensajes de Contacto"
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"{self.nombre} - {self.asunto}"

class ConfiguracionSitio(models.Model):
    """Modelo para configuraciones generales del sitio"""
    titulo_sitio = models.CharField(max_length=200, default="TK REDLINE SPA")
    descripcion_sitio = models.TextField(blank=True)
    palabras_clave = models.TextField(blank=True, help_text="Palabras clave separadas por comas")
    logo_footer = models.ImageField(upload_to='config/', blank=True, null=True)
    fondo_global = models.ImageField(upload_to='config/', blank=True, null=True, help_text="Imagen de fondo global del sitio")
    telefono_footer = models.CharField(max_length=20, blank=True)
    email_footer = models.EmailField(blank=True)
    direccion_footer = models.TextField(blank=True)
    redes_sociales = models.JSONField(default=dict, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Configuración del Sitio"
        verbose_name_plural = "Configuraciones del Sitio"

    def __str__(self):
        return "Configuración del Sitio"

    def save(self, *args, **kwargs):
        if not self.pk and ConfiguracionSitio.objects.exists():
            # Si ya existe una configuración, no crear otra
            return
        super().save(*args, **kwargs)