#!/usr/bin/env python3
import os
import sys
import django
import json

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tekon_website.settings')
django.setup()

from empresa.models import (
    Empresa, Servicio, Proyecto, Cliente, Equipo, 
    Contacto, ConfiguracionSitio
)

def populate_database():
    """Poblar la base de datos con información del PDF"""
    
    # Crear empresa principal
    empresa, created = Empresa.objects.get_or_create(
        nombre="TK REDLINE SPA",
        defaults={
            'slogan': "SOLUCIONES EFICIENTES",
            'descripcion': "TK REDLINE SPA es una empresa especializada en la prestación de servicios generales para el desarrollo de proyectos de ingeniería, construcción, supervisión, fiscalización y capacitación de personal. Nos enfocamos en obras civiles e industriales, incluyendo el desarrollo de sistemas eléctricos y de fibra óptica.",
            'mision': "En TK REDLINE SPA, nos dedicamos a proporcionar soluciones de ingeniería eficientes para maximizar los beneficios en la ejecución de proyectos, optimizando la asignación de recursos y cumpliendo con las leyes y normas vigentes, siempre respetando el medio ambiente.",
            'vision': "Consolidar el prestigio de TK REDLINE SPA como una empresa referente en el ámbito profesional y técnico, contribuyendo al desarrollo y progreso de la región a través de la ejecución de proyectos de alta calidad.",
            'valores': "La honestidad y transparencia son los pilares fundamentales de TK REDLINE SPA en todas nuestras actividades de administración, gestión y coordinación de proyectos.",
            'direccion': "C. Carlos Antúnez 2025, Piso 9-904 – PROVIDENCIA – Santiago de Chile",
            'telefono': "+56 9 3494 9214",
            'email_principal': "mlujan@tekon-rl.cl",
            'email_secundario': "gmartinez@tekon-rl.cl",
            'activo': True
        }
    )
    
    print(f"Empresa {'creada' if created else 'actualizada'}: {empresa.nombre}")
    
    # Crear servicios
    servicios_data = [
        {
            'nombre': 'Administración y Gerenciamiento de Proyectos',
            'descripcion': 'Optimización de recursos, cumplimiento de normas y gestión integral de proyectos de infraestructura.',
            'icono': 'fas fa-project-diagram',
            'orden': 1
        },
        {
            'nombre': 'Supervisión y Fiscalización de Obras',
            'descripcion': 'Control de calidad, seguimiento de proyectos y cumplimiento de especificaciones técnicas.',
            'icono': 'fas fa-clipboard-check',
            'orden': 2
        },
        {
            'nombre': 'Diseño de Ingeniería',
            'descripcion': 'Ingeniería conceptual, básica y de detalle para proyectos de infraestructura básica e industrial.',
            'icono': 'fas fa-drafting-compass',
            'orden': 3
        },
        {
            'nombre': 'Construcción de Obras',
            'descripcion': 'Construcción de obras de infraestructura básica e industrial con materiales modernos.',
            'icono': 'fas fa-hard-hat',
            'orden': 4
        },
        {
            'nombre': 'Auditorías Técnicas',
            'descripcion': 'Evaluación y verificación del cumplimiento de contratos y especificaciones técnicas.',
            'icono': 'fas fa-search',
            'orden': 5
        },
        {
            'nombre': 'Capacitaciones Técnicas',
            'descripcion': 'Formación especializada en gerenciamiento, administración y construcción de proyectos.',
            'icono': 'fas fa-graduation-cap',
            'orden': 6
        }
    ]
    
    for servicio_data in servicios_data:
        servicio, created = Servicio.objects.get_or_create(
            nombre=servicio_data['nombre'],
            defaults=servicio_data
        )
        print(f"Servicio {'creado' if created else 'actualizado'}: {servicio.nombre}")
    
    # Crear proyectos destacados
    proyectos_data = [
        {
            'nombre': 'Supervisión de Telepuertos para SpaceX',
            'descripcion': 'Seguimiento al control de calidad, documentación y Sistema HSE para la construcción de 3 Telepuertos en Buenos Aires y Bahía Blanca.',
            'cliente': 'M&D UNIDOS / SPACEX / PHOENIX TOWER INTERNATIONAL',
            'alcance': 'Supervisión para la construcción de Telepuertos para Bases Satelitales SpaceX',
            'destacado': True
        },
        {
            'nombre': 'Desarrollo de Software para PTI',
            'descripcion': 'Desarrollo de Software de Búsqueda de Locaciones para PTI para TELEFONICA a medida.',
            'cliente': 'PHOENIX TOWER INTERNATIONAL CHILE',
            'alcance': 'Desarrollo de Software y asistencia para el funcionamiento a medida',
            'destacado': True
        },
        {
            'nombre': 'Supervisión de 64 Sitios de Telecomunicaciones',
            'descripcion': 'Seguimiento al control de calidad, documentación y Sistema HSE para la construcción de 64 Radio Bases.',
            'cliente': 'PHOENIX TOWER INTERNATIONAL CHILE',
            'alcance': 'Supervisión para la construcción de 64 Sitios de Telecomunicaciones',
            'destacado': True
        },
        {
            'nombre': 'Ingeniería Básica para Planta Solar Fotovoltaica',
            'descripcion': 'Estudios de Ingeniería Básica, Topografía, Geotecnia y Diseño de Accesos para la Planta Solar.',
            'cliente': 'ENDE CORANI',
            'alcance': 'Estudios de Ingeniería Básica, Topografía, Geotecnia y Diseño de Accesos',
            'destacado': True
        },
        {
            'nombre': 'Teatro Coliseo Cambridge',
            'descripcion': 'Modificación de Ingeniería y Arquitectura para la construcción del TEATRO de 670 butacas y conclusión de Coliseo.',
            'cliente': 'CAMBRIDGE COLLEGE SRL',
            'alcance': 'Rediseño para la Construcción de TEATRO de 670 butacas',
            'destacado': True
        }
    ]
    
    for proyecto_data in proyectos_data:
        proyecto, created = Proyecto.objects.get_or_create(
            nombre=proyecto_data['nombre'],
            defaults=proyecto_data
        )
        print(f"Proyecto {'creado' if created else 'actualizado'}: {proyecto.nombre}")
    
    # Crear clientes
    clientes_data = [
        {
            'nombre': 'Phoenix Tower International',
            'tipo_cliente': 'directo',
            'descripcion': 'Cliente internacional especializado en infraestructura de telecomunicaciones.'
        },
        {
            'nombre': 'SpaceX',
            'tipo_cliente': 'directo',
            'descripcion': 'Empresa aeroespacial líder en tecnología satelital.'
        },
        {
            'nombre': 'Cambridge College',
            'tipo_cliente': 'directo',
            'descripcion': 'Institución educativa de prestigio internacional.'
        },
        {
            'nombre': 'ENDE Corani',
            'tipo_cliente': 'directo',
            'descripcion': 'Empresa estatal de energía de Bolivia.'
        },
        {
            'nombre': 'ENTEL Chile',
            'tipo_cliente': 'directo',
            'descripcion': 'Operador de telecomunicaciones líder en Chile.'
        },
        {
            'nombre': 'CITSA',
            'tipo_cliente': 'directo',
            'descripcion': 'Compañía Industrial de Tabacos S.A.'
        },
        {
            'nombre': 'M&D UNIDOS',
            'tipo_cliente': 'final',
            'descripcion': 'Cliente final en proyectos de telecomunicaciones.'
        },
        {
            'nombre': 'BELMONTE INGENIEROS SRL',
            'tipo_cliente': 'final',
            'descripcion': 'Cliente final en proyectos de ingeniería.'
        }
    ]
    
    for cliente_data in clientes_data:
        cliente, created = Cliente.objects.get_or_create(
            nombre=cliente_data['nombre'],
            defaults=cliente_data
        )
        print(f"Cliente {'creado' if created else 'actualizado'}: {cliente.nombre}")
    
    # Crear equipo
    equipo_data = [
        {
            'nombre': 'J. Manuel Lujan S.',
            'cargo': 'Fundador y Director Ejecutivo',
            'email': 'mlujan@tekon-rl.cl',
            'telefono': '+56 9 3494 9214',
            'descripcion': 'Ingeniero con más de 21 años de experiencia en proyectos de ingeniería, construcción y supervisión. Líder visionario que ha guiado a TK REDLINE SPA hacia la excelencia y la expansión internacional.',
            'orden': 1
        },
        {
            'nombre': 'Gonzalo J. Martinez C.',
            'cargo': 'Socio y Director Técnico',
            'email': 'gmartinez@tekon-rl.cl',
            'telefono': '+56 9 3494 9214',
            'descripcion': 'Ingeniero especializado con amplia experiencia en supervisión de obras y gestión de proyectos. Socio clave en el desarrollo de soluciones eficientes y la expansión de la empresa.',
            'orden': 2
        }
    ]
    
    for miembro_data in equipo_data:
        miembro, created = Equipo.objects.get_or_create(
            nombre=miembro_data['nombre'],
            defaults=miembro_data
        )
        print(f"Miembro del equipo {'creado' if created else 'actualizado'}: {miembro.nombre}")
    
    # Crear configuración del sitio
    configuracion, created = ConfiguracionSitio.objects.get_or_create(
        titulo_sitio="TK REDLINE SPA",
        defaults={
            'descripcion_sitio': 'TK REDLINE SPA - Soluciones Eficientes en Ingeniería, Construcción y Supervisión',
            'palabras_clave': 'ingeniería, construcción, supervisión, fiscalización, telecomunicaciones, infraestructura, Chile, Argentina',
            'telefono_footer': '+56 9 3494 9214',
            'email_footer': 'mlujan@tekon-rl.cl',
            'direccion_footer': 'C. Carlos Antúnez 2025, Piso 9-904 – PROVIDENCIA – Santiago de Chile',
            'redes_sociales': {
                'linkedin': '#',
                'facebook': '#',
                'twitter': '#'
            },
            'activo': True
        }
    )
    
    print(f"Configuración del sitio {'creada' if created else 'actualizada'}")
    
    print("\n¡Base de datos poblada exitosamente!")

if __name__ == "__main__":
    populate_database()



