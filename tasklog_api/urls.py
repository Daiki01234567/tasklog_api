from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/projects/", include(("projects.urls", "projects"), namespace="projects")),
    path("api/tasks/",    include(("tasks.urls", "tasks"),     namespace="tasks")),
    path("api/reports/",  include(("worklogs.urls", "reports"), namespace="reports")),
]
