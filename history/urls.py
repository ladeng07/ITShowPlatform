from django.conf.urls.static import static
from ITShowPlatform import settings
from django.urls import path
from history.views import DepartmentViewSet, MemberViewSet, HistoryViewSet

urlpatterns = [

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
