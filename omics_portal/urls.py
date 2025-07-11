"""
URL configuration for omics_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

urlpatterns = [
    # Django admin
    path('admin_tools/', include('admin_tools.urls')),
    path('admin/', admin.site.urls),
    # User management
    path('accounts/', include('allauth.urls')),

    # Local apps
    path('', include('pages.urls')),

    # for "kokoro" app
    path("kokoro/", include("kokoro.urls"), name="kokoro"), 
    # for "patients" app
    path("patients/", include("patients.urls")),
    
    path('submissions/', include(('submissions.urls', 'submissions'), namespace='submissions')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)