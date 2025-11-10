from .models import Empresa, ConfiguracionSitio
from .utils.site_resolver import resolve_site

def empresa_context(request):
    """Contexto global para información de la empresa"""
    current_site = resolve_site(request)
    site_domain = current_site.domain.split(':')[0].lower() if current_site else ''
    return {
        'empresa': Empresa.objects.filter(site=current_site, activo=True).first(),
        'configuracion': ConfiguracionSitio.objects.filter(site=current_site, activo=True).first(),
        'current_site': current_site,
        'site_domain': site_domain,
    }



