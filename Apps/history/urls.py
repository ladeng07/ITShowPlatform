from django.conf.urls.static import static
from ITShowPlatform import settings
from django.urls import path
from Apps.history.views import DepartmentViewSet, MemberViewSet, HistoryViewSet

urlpatterns = [
    path('department/', DepartmentViewSet.as_view()),
    path('member/', MemberViewSet.as_view()),
    path('history/', HistoryViewSet.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
