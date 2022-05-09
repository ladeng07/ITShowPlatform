"""ITShowPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.views.static import serve
from ITShowPlatform import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/api/', include('apps.comments.urls')),
    path('v1/api/', include('apps.history.urls')),
    path('v1/api/', include('apps.enroll.urls')),
    path('v1/api/', include('apps.work.urls')),
    path(r'^api-auth/', include('rest_framework.urls')),
    re_path(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
]
