from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from .models import (
    Empresa, Servicio, Proyecto, Cliente, Equipo, 
    Contacto, ConfiguracionSitio
)
from .utils.site_resolver import resolve_site

def home(request):
    """Vista principal de la página de inicio"""
    current_site = resolve_site(request)
    empresa = Empresa.objects.filter(site=current_site, activo=True).first()
    servicios = Servicio.objects.filter(activo=True).order_by('orden')[:6]
    proyectos_destacados = Proyecto.objects.filter(activo=True, destacado=True).order_by('orden', '-fecha_creacion')[:3]
    clientes_queryset = Cliente.objects.filter(
        activo=True,
        destacado=True,
        logo__isnull=False,
    ).exclude(logo='').order_by('orden', 'nombre')
    if not clientes_queryset.exists():
        clientes_queryset = Cliente.objects.filter(
            activo=True,
            logo__isnull=False,
        ).exclude(logo='').order_by('orden', 'nombre')
    clientes = list(clientes_queryset)
    equipo = Equipo.objects.filter(activo=True, socio=True).order_by('orden')[:4]
    configuracion = ConfiguracionSitio.objects.filter(site=current_site, activo=True).first()
    
    context = {
        'empresa': empresa,
        'servicios': servicios,
        'proyectos_destacados': proyectos_destacados,
        'clientes': clientes,
        'equipo': equipo,
        'configuracion': configuracion,
    }
    return render(request, 'empresa/home.html', context)

def servicios(request):
    """Vista de la página de servicios"""
    servicios = Servicio.objects.filter(activo=True).order_by('orden')
    current_site = resolve_site(request)
    empresa = Empresa.objects.filter(site=current_site, activo=True).first()
    configuracion = ConfiguracionSitio.objects.filter(site=current_site, activo=True).first()
    
    context = {
        'servicios': servicios,
        'empresa': empresa,
        'configuracion': configuracion,
    }
    return render(request, 'empresa/servicios.html', context)

def proyectos(request):
    """Vista de la página de proyectos"""
    proyectos = Proyecto.objects.filter(activo=True).order_by('orden', '-fecha_creacion')
    current_site = resolve_site(request)
    empresa = Empresa.objects.filter(site=current_site, activo=True).first()
    configuracion = ConfiguracionSitio.objects.filter(site=current_site, activo=True).first()
    
    context = {
        'proyectos': proyectos,
        'empresa': empresa,
        'configuracion': configuracion,
    }
    return render(request, 'empresa/proyectos.html', context)

def clientes(request):
    """Vista de la página de clientes"""
    clientes_directos = Cliente.objects.filter(activo=True, tipo_cliente='directo').order_by('orden', 'nombre')
    clientes_finales = Cliente.objects.filter(activo=True, tipo_cliente='final').order_by('orden', 'nombre')
    clientes_destacados = Cliente.objects.filter(activo=True, destacado=True).order_by('orden', 'nombre')
    current_site = resolve_site(request)
    empresa = Empresa.objects.filter(site=current_site, activo=True).first()
    configuracion = ConfiguracionSitio.objects.filter(site=current_site, activo=True).first()
    
    context = {
        'clientes_directos': clientes_directos,
        'clientes_finales': clientes_finales,
        'clientes_destacados': clientes_destacados,
        'empresa': empresa,
        'configuracion': configuracion,
    }
    return render(request, 'empresa/clientes.html', context)

def equipo(request):
    """Vista de la página del equipo"""
    equipo = Equipo.objects.filter(activo=True).order_by('orden')
    current_site = resolve_site(request)
    empresa = Empresa.objects.filter(site=current_site, activo=True).first()
    configuracion = ConfiguracionSitio.objects.filter(site=current_site, activo=True).first()
    
    context = {
        'equipo': equipo,
        'empresa': empresa,
        'configuracion': configuracion,
    }
    return render(request, 'empresa/equipo.html', context)

def contacto(request):
    """Vista de la página de contacto"""
    current_site = resolve_site(request)
    empresa = Empresa.objects.filter(site=current_site, activo=True).first()
    configuracion = ConfiguracionSitio.objects.filter(site=current_site, activo=True).first()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono', '')
        empresa_cliente = request.POST.get('empresa', '')
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')
        
        # Crear el mensaje de contacto
        contacto_obj = Contacto.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            empresa=empresa_cliente,
            asunto=asunto,
            mensaje=mensaje
        )
        
        # Enviar email de notificación
        try:
            send_mail(
                f'Nuevo mensaje de contacto: {asunto}',
                f'Nombre: {nombre}\nEmail: {email}\nTeléfono: {telefono}\nEmpresa: {empresa_cliente}\n\nMensaje:\n{mensaje}',
                settings.DEFAULT_FROM_EMAIL,
                [empresa.email_principal if empresa else 'mlujan@tekon-rl.cl'],
                fail_silently=False,
            )
            messages.success(request, '¡Mensaje enviado correctamente! Nos pondremos en contacto contigo pronto.')
        except Exception as e:
            messages.warning(request, 'El mensaje se guardó correctamente, pero hubo un problema al enviar el email.')
        
        return redirect('contacto')
    
    context = {
        'empresa': empresa,
        'configuracion': configuracion,
    }
    return render(request, 'empresa/contacto.html', context)

def sobre_nosotros(request):
    """Vista de la página sobre nosotros"""
    current_site = resolve_site(request)
    empresa = Empresa.objects.filter(site=current_site, activo=True).first()
    equipo = Equipo.objects.filter(activo=True, socio=True).order_by('orden')
    configuracion = ConfiguracionSitio.objects.filter(site=current_site, activo=True).first()
    
    context = {
        'empresa': empresa,
        'equipo': equipo,
        'configuracion': configuracion,
    }
    return render(request, 'empresa/sobre_nosotros.html', context)