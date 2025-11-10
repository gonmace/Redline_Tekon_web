from .models import Empresa, ConfiguracionSitio

def empresa_context(request):
    """Contexto global para información de la empresa"""
    return {
        'empresa': Empresa.objects.filter(activo=True).first(),
        'configuracion': ConfiguracionSitio.objects.filter(activo=True).first(),
    }



