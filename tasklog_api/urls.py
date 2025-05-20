from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/projects/', include(('projects.urls', 'projects'), namespace='projects')),
    path('api/tasks/', include(('tasks.urls', 'tasks'),     namespace='tasks')),
    path('api/reports/', include(('worklogs.urls', 'reports'), namespace='reports')),
    
    # YOUR PATTERNS
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
