from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='TaskLog API',
        default_version='v1',
        description='タスク＆工数管理 API ドキュメント',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/users/', include(('users.urls'), 'users'), namespace='users'),
    path('api/projects/', include(('projects.urls', 'projects'), namespace='projects')),
    path('api/tasks/',    include(('tasks.urls', 'tasks'),     namespace='tasks')),
    path('api/reports/',  include(('worklogs.urls', 'reports'), namespace='reports')),
    
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/',   schema_view.with_ui('redoc',   cache_timeout=0), name='schema-redoc'),
]
