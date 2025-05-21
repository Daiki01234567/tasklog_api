from users.tests.factory import UserFactory, SuperUserFactory
from django.db import IntegrityError
from users.models import User

import pytest

@pytest.mark.django_db
class TestUser(object):

    def setup_method(self):
        self.user = UserFactory()
        self.db_user = User.objects.get(pk=self.user.pk)

    def test_create_user(self):
        assert self.db_user.role == 'ACC'
        assert self.db_user.is_active is True
        assert self.db_user.is_staff is False
        assert self.db_user.is_superuser is False
        assert self.db_user.check_password('Password123') is True

    def test_create_user_in_role(self):
        user = User.objects.create_user(
            email='test@mail.com',
            role='PM',
            password=self.db_user.password
        )
        assert user.role == 'ACC'

    def test_create_user_raise_integrity_error(self):
        with pytest.raises(IntegrityError):
            User.objects.create_user(email=self.db_user.email, password='Password123')

    def test_create_superuser(self):
        superuser = SuperUserFactory()
        db_superuser = User.objects.get(pk=superuser.pk)
        assert db_superuser.role == 'PM'
        assert db_superuser.is_staff is True
        assert db_superuser.is_superuser is True

    def test_str_return(self):
        assert str(self.user) == self.db_user.email
