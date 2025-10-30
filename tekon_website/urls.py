"""
URL configuration for tekon_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render

def test_tailwind(request):
    return render(request, 'test_tailwind.html')

def demo_daisyui(request):
    return render(request, 'demo_daisyui.html')

def demo_moderno(request):
    return render(request, 'demo_moderno.html')

def test_theme(request):
    return render(request, 'test_theme.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-tailwind/', test_tailwind, name='test_tailwind'),
    path('demo-daisyui/', demo_daisyui, name='demo_daisyui'),
    path('demo-moderno/', demo_moderno, name='demo_moderno'),
    path('test-theme/', test_theme, name='test_theme'),
    path('', include('empresa.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
