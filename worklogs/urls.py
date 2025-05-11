from django.urls import path, include
from .views import WorkLogViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', WorkLogViewSet, basename='worklog')

urlpatterns = [
    path('', include(router.urls)),
]
