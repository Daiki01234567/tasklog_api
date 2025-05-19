from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('メールアドレスは必須です')
        
        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.role = 'PM'
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        PM = 'PM', 'PM'
        DEV = 'DEV', 'DEV'
        ACC = 'ACC', 'ACC'
    
    email = models.EmailField(unique=True, blank=False, max_length=254)
    role = models.CharField(max_length=3, choices=Role.choices, default='ACC')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']
    
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
