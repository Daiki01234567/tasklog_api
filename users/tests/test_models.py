from users.tests.factory import UserFactory, SuperUserFactory
from django.db import IntegrityError
from users.models import User

import pytest

@pytest.mark.django_db
class TestUser(object):

    def setup_method(self):
        self.user = UserFactory()

    def test_create_user(self):
        assert isinstance(self.user, User)
        assert self.user.role == 'ACC'
        assert self.user.is_active is True
        assert self.user.is_staff is False
        assert self.user.is_superuser is False
        assert self.user.check_password('Password123') is True

    def test_create_user_raise_integrity_error(self):
        with pytest.raises(IntegrityError):
            User.objects.create_user(email=self.user.email, password='Password123')

    def test_create_superuser(self):
        superuser = SuperUserFactory()
        assert superuser.role == 'PM'
        assert superuser.is_staff is True
        assert superuser.is_superuser is True

    def test_str_return(self):
        assert str(self.user) == self.user.email
