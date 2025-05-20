import factory
from users.models import User

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'Password123')
    role = 'ACC'
    is_active = True
    is_staff = False
    is_superuser = False

class SuperUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        
    email = factory.Sequence(lambda n: f'admin{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'Password123')
    
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return model_class.objects.create_superuser(*args, **kwargs)
