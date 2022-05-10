from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from ITShowPlatform import settings


urlpatterns = [
    path('work/', views.Work.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

