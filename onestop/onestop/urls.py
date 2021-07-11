"""onestop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from dictionary import views
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('admin/', admin.site.urls),
    path('comments/', include('django_comments_xtd.urls')),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('under-construction/', views.under_construction, name='under-construction'),
    path('help/',
         views.TemplateView.as_view(template_name="onestop/help.html"), name='help'),
    path('privacy-policy/',
         views.TemplateView.as_view(template_name="onestop/privacy_policy.html"), name='privacy-policy'),
    path('terms-and-conditions/',
         views.TemplateView.as_view(template_name="onestop/terms_and_conditions.html"), name='terms-and-conditions'),
    path('dictionary/', include('dictionary.urls')),
    path('blog/', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('summernote/', include('django_summernote.urls')),
]

#To serve media files in developmnt:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)