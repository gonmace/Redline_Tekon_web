import json

from django.contrib import admin
from django.http import HttpResponse
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.utils.html import format_html
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
            'fields': ('imagen_principal', 'imagen_fondo_hero'),
            'description': 'Imagen Principal: Se muestra en la sección hero. Imagen Fondo Hero: Imagen de fondo para la sección hero.'
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Servicio)
class ServicioAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['nombre', 'orden', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']
    ordering = ['orden', 'nombre']
    sortable = 'orden'

@admin.register(Proyecto)
class ProyectoAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['nombre', 'cliente', 'destacado', 'activo', 'orden', 'fecha_creacion']
    list_filter = ['activo', 'destacado', 'fecha_creacion']
    search_fields = ['nombre', 'cliente', 'descripcion']
    list_editable = ['destacado', 'activo']
    ordering = ['orden', '-fecha_creacion']
    sortable = 'orden'
    
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

    def update_order(self, request):
        response = super().update_order(request)
        if getattr(response, 'status_code', None) != 400:
            return response

        updated_items_raw = request.POST.get('updatedItems')
        if not updated_items_raw:
            return response

        try:
            updated_items = json.loads(updated_items_raw)
        except json.JSONDecodeError:
            return response

        extra_filters = self.get_extra_model_filters(request)
        num_updated = self._update_order(updated_items, extra_filters)
        return HttpResponse(f"Updated {num_updated} items")

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['logo_preview', 'nombre', 'tipo_cliente', 'activo', 'fecha_creacion']
    list_filter = ['tipo_cliente', 'activo', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['activo']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="height:48px;width:auto;border-radius:8px;object-fit:contain;background:linear-gradient(135deg, rgba(248,250,252,.9), rgba(226,232,240,.4));padding:6px;box-shadow:0 4px 12px -6px rgba(15,23,42,.35);" alt="{}" />',
                obj.logo.url,
                obj.nombre,
            )
        return format_html(
            '<span style="display:inline-block;padding:6px 10px;border-radius:9999px;background:rgba(226,232,240,.6);font-size:12px;color:rgba(15,23,42,.58);text-transform:uppercase;letter-spacing:.08em;">Sin logo</span>'
        )

    logo_preview.short_description = "Logo"
    logo_preview.admin_order_field = 'logo'

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['foto_thumb', 'nombre', 'cargo', 'email', 'activo', 'orden']
    list_filter = ['activo', 'fecha_creacion']
    search_fields = ['nombre', 'cargo', 'email']
    list_editable = ['orden', 'activo']
    ordering = ['orden', 'nombre']
    readonly_fields = ['foto_preview']

    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'cargo', 'descripcion', 'orden', 'activo')
        }),
        ('Contacto', {
            'fields': ('email', 'telefono')
        }),
        ('Fotografía', {
            'fields': ('foto', 'foto_preview'),
            'description': 'Sube una imagen representativa del miembro del equipo (recomendado 400x400px).'
        }),
    )

    def foto_preview(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-height:120px;border-radius:16px;box-shadow:0 10px 25px -18px rgba(15,23,42,.55);" />', obj.foto.url)
        return format_html('<span style="color:rgba(15,23,42,.45);font-size:13px;">Sin fotografía cargada</span>')

    foto_preview.short_description = "Vista previa"

    def foto_thumb(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="height:34px;width:34px;border-radius:50%;object-fit:cover;box-shadow:0 6px 12px -8px rgba(15,23,42,.45);" />', obj.foto.url)
        return format_html('<span style="color:rgba(15,23,42,.45);font-size:12px;">Sin foto</span>')

    foto_thumb.short_description = "Foto"

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
        ('Apariencia Global', {
            'fields': ('fondo_global',),
            'description': 'Imagen de fondo global del sitio (cover, centered)'
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