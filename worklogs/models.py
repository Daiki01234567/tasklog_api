from django.db import models
from users.models import User
from tasks.models import Task

class WorkLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_date = models.DateField()
    spent_hours = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        verbose_name = verbose_name_plural = 'ログ'
        constraints = [
            models.UniqueConstraint(
                fields=['task', 'work_date'], 
                name='unique_together'
            ),
            models.CheckConstraint(
                check=models.Q(spent_hours__gte=0),
                name='worklog_spent_hours__gte_0'
            )
        ]
        
    def __str__(self):
        return f'{self.user.email}  {self.task.title}'
