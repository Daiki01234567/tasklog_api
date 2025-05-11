from django.db import models
from users.models import User
from projects.models import Project

class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'TODO', 'TODO'
        DOING = 'DOING', 'DOING'
        DONE = 'DONE', 'DONE'
    
    project = models.ForeignKey(Project, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    planned_hours = models.PositiveIntegerField(null=False, blank=False) 
    assignee = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=5, choices=Status.choices, default=Status.TODO)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = verbose_name_plural = 'タスク'
        indexes = [
            models.Index(
                fields=['project', 'status'], 
                name='idx_task_project_status'
            ),
            models.Index(
                fields=['assignee', 'due_date'],
                name='idx_task_assignee_due'
            )
        ]
        constraints = [
            models.UniqueConstraint(
              fields=['project', 'title'],
              name='uniq_task_title_per_project',
            ),
            models.CheckConstraint(
                check=models.Q(planned_hours__gte=0),
                name='task_planned_hours__gte_0'
            )
        ]
        
    def __str__(self):
        return f'{self.project.name}  {self.title}'