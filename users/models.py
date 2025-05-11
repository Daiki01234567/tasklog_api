from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password

class User(AbstractUser):
    class Role(models.TextChoices):
        PM = 'PM', 'PM'
        DEV = 'DEV', 'DEV'
        ACC = 'ACC', 'ACC'
    
    email = models.EmailField(unique=True, blank=False, max_length=254)
    role = models.CharField(max_length=3, choices=Role.choices, default='ACC')
    first_name = None
    last_name = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    
    class Meta:
        verbose_name = verbose_name_plural = 'ユーザー'
        indexes = [
            models.Index(fields=['role'], name='idx_user_role'),
        ]

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2'):
            self.set_password(self.password)
        super().save(*args, **kwargs)