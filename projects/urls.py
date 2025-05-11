from django.urls import path, include
from .views import ProjectViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='project')

urlpatterns = [
    path('', include(router.urls)),
]
