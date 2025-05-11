from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = verbose_name_plural = 'プロジェクト'
        indexes = [
            models.Index(fields=['name'], name='idx_project_name')
        ]
    
    def __str__(self):
        return self.name