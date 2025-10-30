from django.contrib import admin
from .models import (
    Empresa, Servicio, Proyecto, Cliente, Equipo, 
    Contacto, ConfiguracionSitio
)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'email_principal', 'activo', 'fecha_actualizacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'email_principal']
    readonly_fields = ['fecha_creacion', 'fecha_actualizacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'slogan', 'descripcion', 'activo')
        }),
        ('Misión, Visión y Valores', {
            'fields': ('mision', 'vision', 'valores')
        }),
        ('Contacto', {
            'fields': ('direccion', 'telefono', 'email_principal', 'email_secundario')
        }),
        ('Imágenes', {
            'fields': ('logo', 'imagen_principal', 'imagen_fondo_hero'),
            'description': 'Logo: Se muestra en la navegación. Imagen Principal: Se muestra en la sección hero. Imagen Fondo Hero: Imagen de fondo para la sección hero.'
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'orden', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['orden', 'activo']
    ordering = ['orden', 'nombre']

@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cliente', 'destacado', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'destacado', 'fecha_creacion']
    search_fields = ['nombre', 'cliente', 'descripcion']
    list_editable = ['destacado', 'activo']
    ordering = ['-fecha_creacion']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'cliente', 'alcance')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Configuración', {
            'fields': ('imagen', 'destacado', 'activo')
        }),
    )

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tipo_cliente', 'activo', 'fecha_creacion']
    list_filter = ['tipo_cliente', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cargo', 'email', 'activo', 'orden']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'cargo', 'email']
    list_editable = ['orden', 'activo']
    ordering = ['orden', 'nombre']

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'asunto', 'leido', 'respondido', 'fecha_envio']
    list_filter = ['leido', 'respondido', 'fecha_envio']
    search_fields = ['nombre', 'email', 'asunto', 'mensaje']
    readonly_fields = ['fecha_envio']
    list_editable = ['leido', 'respondido']
    ordering = ['-fecha_envio']
    
    fieldsets = (
        ('Información del Contacto', {
            'fields': ('nombre', 'email', 'telefono', 'empresa')
        }),
        ('Mensaje', {
            'fields': ('asunto', 'mensaje')
        }),
        ('Estado', {
            'fields': ('leido', 'respondido', 'fecha_envio')
        }),
    )

@admin.register(ConfiguracionSitio)
class ConfiguracionSitioAdmin(admin.ModelAdmin):
    list_display = ['titulo_sitio', 'activo']
    fieldsets = (
        ('Información General', {
            'fields': ('titulo_sitio', 'descripcion_sitio', 'palabras_clave', 'activo')
        }),
        ('Footer', {
            'fields': ('logo_footer', 'telefono_footer', 'email_footer', 'direccion_footer')
        }),
        ('Redes Sociales', {
            'fields': ('redes_sociales',)
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir una configuración
        return not ConfiguracionSitio.objects.exists()