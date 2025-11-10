from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site


def resolve_site(request):
    """Return the Site matching the current request, ignoring port numbers."""
    host = request.get_host().split(':')[0].lower()

    current_site = getattr(request, 'site', None)
    if current_site and current_site.domain.split(':')[0].lower() == host:
        return current_site

    try:
        return Site.objects.get(domain__iexact=host)
    except Site.DoesNotExist:
        return get_current_site(request)
